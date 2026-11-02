from __future__ import annotations

import argparse
import sys
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
    return len(host_labels) == len(suffix_labels) + 1 and host_labels[1:] == suffix_labels


def _list(value: object, *, field: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def validate_document(document: object, public_host: str) -> None:
    if not isinstance(document, dict):
        raise ValueError("desired state must be a mapping")
    spec = document.get("spec")
    if not isinstance(spec, dict):
        raise ValueError("desired state spec must be a mapping")

    certificates: dict[str, list[str]] = {}
    for index, certificate in enumerate(_list(spec.get("certificates"), field="spec.certificates")):
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
            raise ValueError(f"certificate {resource_id} must cover at least one domain")
        if resource_id in certificates:
            raise ValueError(f"duplicate certificate resource_id: {resource_id}")
        certificates[resource_id] = domains

    requested_public_host = _hostname(public_host, field="public-host")
    observed_public_hosts: set[str] = set()
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
            if not any(certificate_covers(domain, pattern) for pattern in certificate_domains)
        ]
        if uncovered:
            raise ValueError(
                f"certificate {certificate_ref} does not cover proxy hostname(s): "
                f"{', '.join(uncovered)}"
            )

    if requested_public_host not in observed_public_hosts:
        raise ValueError(
            f"public-host {requested_public_host} is not declared by spec.proxyHosts.domain_names"
        )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--desired-state", type=Path, required=True)
    parser.add_argument("--public-host", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        document = yaml.safe_load(args.desired_state.read_text(encoding="utf-8"))
        validate_document(document, args.public_host)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"TLS coverage validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"TLS coverage validated for {args.public_host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
