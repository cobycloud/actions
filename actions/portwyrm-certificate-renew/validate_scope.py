from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def certificate_provider(certificate: dict[str, Any]) -> str:
    """Resolve the provider from supported Wyrmctl certificate representations."""

    api_payload = certificate.get("api_payload")
    api_provider = api_payload.get("provider") if isinstance(api_payload, dict) else None
    for value in (
        certificate.get("certificate_type"),
        certificate.get("provider"),
        api_provider,
    ):
        if isinstance(value, str) and value.strip():
            return value.strip().casefold()
    return ""


def validate_scope(
    desired_path: Path,
    expected_owner: str,
    expected_resource_id: str,
) -> dict[str, Any]:
    payload = yaml.safe_load(desired_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("desired state must be a mapping")
    spec = payload.get("spec")
    if not isinstance(spec, dict):
        raise ValueError("desired state spec must be a mapping")
    raw_certificates = spec.get("certificates", [])
    if not isinstance(raw_certificates, list):
        raise ValueError("desired state spec.certificates must be an array")
    certificates = [
        item
        for item in raw_certificates
        if isinstance(item, dict)
        and isinstance(item.get("meta"), dict)
        and item["meta"].get("owner") == expected_owner
        and item["meta"].get("resource_id") == expected_resource_id
    ]
    if len(certificates) != 1:
        raise ValueError(
            "renewal requires exactly one certificate matching the reviewed "
            f"owner and resource_id; found {len(certificates)}"
        )
    certificate = certificates[0]
    provider = certificate_provider(certificate)
    if provider != "letsencrypt":
        raise ValueError(
            "only letsencrypt certificates may use this renewal workflow; "
            f"resolved provider was {provider or 'unset'}"
        )
    domains = certificate.get("domain_names", [])
    if (
        not isinstance(domains, list)
        or not domains
        or any(not isinstance(domain, str) or not domain.strip() for domain in domains)
        or len(domains) != len(set(domains))
    ):
        raise ValueError("certificate domains must be present, non-empty, and unique")
    return {
        "desired_state": str(desired_path),
        "owner": expected_owner,
        "resource_id": expected_resource_id,
        "certificate_name": certificate.get("name"),
        "domain_names": domains,
        "provider": provider,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("desired_state", type=Path)
    parser.add_argument("owner")
    parser.add_argument("resource_id")
    parser.add_argument("evidence_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        evidence = validate_scope(args.desired_state, args.owner, args.resource_id)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Certificate renewal scope validation failed: {exc}")
        return 1
    args.evidence_path.parent.mkdir(parents=True, exist_ok=True)
    args.evidence_path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
