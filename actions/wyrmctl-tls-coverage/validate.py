from __future__ import annotations

import argparse
import hashlib
import socket
import ssl
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml


def _hostname(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must contain a non-empty hostname")
    hostname = value.strip().lower().rstrip(".")
    if "://" in hostname or "/" in hostname or ":" in hostname:
        raise ValueError(f"{field} must be a hostname without a scheme, path, or port")
    return hostname


def certificate_covers(hostname: str, certificate_name: str) -> bool:
    host = _hostname(hostname, field="proxy hostname")
    pattern = _hostname(certificate_name, field="certificate domain")
    if pattern == host:
        return True
    if not pattern.startswith("*.") or pattern.count("*") != 1:
        return False
    suffix = pattern[2:]
    host_labels = host.split(".")
    suffix_labels = suffix.split(".")
    return (
        len(host_labels) == len(suffix_labels) + 1 and host_labels[1:] == suffix_labels
    )


def _reject_gateway_identity(
    hostname: str,
    *,
    field: str,
    application_domains: tuple[str, ...] = (),
) -> None:
    identity = _hostname(hostname, field=field)
    first_label = identity.split(".", 1)[0]
    if first_label == "portwyrm" or first_label.startswith("portwyrm-"):
        if any(certificate_covers(domain, identity) for domain in application_domains):
            return
        raise ValueError(
            f"{field} must identify the application, not a Portwyrm gateway"
        )


def _list(value: object, *, field: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def validate_document(document: object, public_host: str) -> dict[str, tuple[str, ...]]:
    if not isinstance(document, dict):
        raise ValueError("desired state must be a mapping")
    spec = document.get("spec")
    if not isinstance(spec, dict):
        raise ValueError("desired state spec must be a mapping")

    certificates: dict[str, list[str]] = {}
    for index, certificate in enumerate(
        _list(spec.get("certificates"), field="spec.certificates")
    ):
        if not isinstance(certificate, dict):
            raise ValueError(f"spec.certificates[{index}] must be a mapping")
        meta = certificate.get("meta")
        resource_id = meta.get("resource_id") if isinstance(meta, dict) else None
        if not isinstance(resource_id, str) or not resource_id.strip():
            raise ValueError(f"spec.certificates[{index}].meta.resource_id is required")
        domains = [
            _hostname(item, field=f"certificate {resource_id} domain_names")
            for item in _list(
                certificate.get("domain_names"),
                field=f"certificate {resource_id} domain_names",
            )
        ]
        if not domains:
            raise ValueError(
                f"certificate {resource_id} must cover at least one domain"
            )
        if resource_id in certificates:
            raise ValueError(f"duplicate certificate resource_id: {resource_id}")
        certificates[resource_id] = domains

    requested_public_host = _hostname(public_host, field="public-host")
    observed_public_hosts: set[str] = set()
    certificate_bindings: dict[str, set[str]] = {}
    proxy_hosts = _list(spec.get("proxyHosts"), field="spec.proxyHosts")
    if not proxy_hosts:
        raise ValueError("spec.proxyHosts must contain at least one public proxy host")

    for index, proxy in enumerate(proxy_hosts):
        if not isinstance(proxy, dict):
            raise ValueError(f"spec.proxyHosts[{index}] must be a mapping")
        domains = [
            _hostname(item, field=f"proxyHosts[{index}].domain_names")
            for item in _list(
                proxy.get("domain_names"),
                field=f"proxyHosts[{index}].domain_names",
            )
        ]
        if not domains:
            raise ValueError(f"proxyHosts[{index}] must expose at least one domain")
        observed_public_hosts.update(domains)

        certificate_ref = proxy.get("certificate_ref")
        if not isinstance(certificate_ref, str) or not certificate_ref.strip():
            raise ValueError(
                f"proxyHosts[{index}] ({', '.join(domains)}) has no certificate_ref"
            )
        certificate_domains = certificates.get(certificate_ref)
        if certificate_domains is None:
            raise ValueError(
                f"proxyHosts[{index}] references unknown certificate {certificate_ref}"
            )
        uncovered = [
            domain
            for domain in domains
            if not any(
                certificate_covers(domain, pattern) for pattern in certificate_domains
            )
        ]
        if uncovered:
            raise ValueError(
                f"certificate {certificate_ref} does not cover proxy hostname(s): "
                f"{', '.join(uncovered)}"
            )
        certificate_bindings.setdefault(certificate_ref, set()).update(domains)

    if requested_public_host not in observed_public_hosts:
        raise ValueError(
            f"public-host {requested_public_host} is not declared by spec.proxyHosts.domain_names"
        )
    for reference, application_domains in certificate_bindings.items():
        _reject_gateway_identity(
            certificates[reference][0],
            field=f"certificate {reference} primary domain",
            application_domains=tuple(sorted(application_domains)),
        )
    return {
        reference: tuple(sorted(domains))
        for reference, domains in sorted(certificate_bindings.items())
    }


PeerCertificateFetcher = Callable[
    [str, int, float],
    tuple[str, tuple[str, ...], str],
]


def fetch_peer_certificate(
    hostname: str, port: int, timeout: float
) -> tuple[str, tuple[str, ...], str]:
    """Return a trusted SNI peer certificate fingerprint, DNS SANs, and subject CN."""

    context = ssl.create_default_context()
    with (
        socket.create_connection((hostname, port), timeout=timeout) as connection,
        context.wrap_socket(connection, server_hostname=hostname) as tls,
    ):
        certificate = tls.getpeercert()
        der = tls.getpeercert(binary_form=True)
    if not der:
        raise ValueError(f"{hostname}:{port} returned no peer certificate")
    sans = tuple(
        _hostname(value, field=f"live certificate SAN for {hostname}")
        for kind, value in certificate.get("subjectAltName", ())
        if kind == "DNS"
    )
    common_names = tuple(
        _hostname(value, field=f"live certificate common name for {hostname}")
        for rdn in certificate.get("subject", ())
        for key, value in rdn
        if key == "commonName"
    )
    if len(common_names) != 1:
        raise ValueError(
            f"{hostname}:{port} must return exactly one subject common name"
        )
    return hashlib.sha256(der).hexdigest(), sans, common_names[0]


def verify_live_bindings(
    bindings: dict[str, tuple[str, ...]],
    *,
    port: int = 443,
    timeout: float = 15.0,
    fetcher: PeerCertificateFetcher = fetch_peer_certificate,
) -> dict[str, str]:
    """Verify every proxy hostname and require one live certificate per reference."""

    fingerprints: dict[str, str] = {}
    for reference, domains in bindings.items():
        reference_fingerprint: str | None = None
        for domain in domains:
            try:
                fingerprint, sans, common_name = fetcher(domain, port, timeout)
            except (OSError, ssl.SSLError, ValueError) as exc:
                raise ValueError(
                    f"live TLS verification failed for {domain} bound to {reference}: {exc}"
                ) from exc
            if not any(certificate_covers(domain, pattern) for pattern in sans):
                raise ValueError(
                    f"live certificate for {domain} bound to {reference} does not cover the hostname"
                )
            _reject_gateway_identity(
                common_name,
                field=f"live certificate common name for {domain}",
                application_domains=domains,
            )
            if not any(
                certificate_covers(bound_domain, common_name)
                for bound_domain in domains
            ):
                raise ValueError(
                    f"live certificate common name {common_name} for {domain} "
                    "does not identify an application hostname bound to the certificate"
                )
            if reference_fingerprint is None:
                reference_fingerprint = fingerprint
            elif fingerprint != reference_fingerprint:
                raise ValueError(
                    f"proxy hostnames bound to {reference} serve different live certificates"
                )
        if reference_fingerprint is None:
            raise ValueError(
                f"certificate reference {reference} has no proxy hostnames"
            )
        fingerprints[reference] = reference_fingerprint
    return fingerprints


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--desired-state", type=Path, required=True)
    parser.add_argument("--public-host", required=True)
    parser.add_argument("--verify-live", choices=("true", "false"), default="false")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--timeout", type=float, default=15.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        document = yaml.safe_load(args.desired_state.read_text(encoding="utf-8"))
        bindings = validate_document(document, args.public_host)
        fingerprints = (
            verify_live_bindings(bindings, port=args.port, timeout=args.timeout)
            if args.verify_live == "true"
            else {}
        )
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"TLS coverage validation failed: {exc}", file=sys.stderr)
        return 1
    if fingerprints:
        print(
            "Live TLS coverage validated for "
            f"{sum(len(domains) for domains in bindings.values())} proxy hostname(s) "
            f"across {len(fingerprints)} referenced certificate(s)"
        )
    else:
        print(f"TLS coverage validated for {args.public_host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
