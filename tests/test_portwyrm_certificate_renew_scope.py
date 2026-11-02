from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "actions/portwyrm-certificate-renew/validate_scope.py"
SPEC = importlib.util.spec_from_file_location("portwyrm_certificate_renew_scope", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


ACTUAL_CONSUMER_SCHEMA = """
spec:
  certificates:
    - name: memdedupe.engine-demo.tigrbl.dev
      domain_names:
        - memdedupe.engine-demo.tigrbl.dev
        - dedupe.engine-demo.tigrbl.dev
      certificate_type: letsencrypt
      api_payload:
        provider: letsencrypt
      meta:
        managed_by: wyrmctl
        owner: tigrbl-memdedupe-engine-demo
        resource_id: cert.tigrbl-memdedupe-engine-demo
"""


def write_consumer_state(tmp_path: Path, document: str = ACTUAL_CONSUMER_SCHEMA) -> Path:
    path = tmp_path / "desired-state.yaml"
    path.write_text(document, encoding="utf-8")
    return path


def test_accepts_actual_consumer_certificate_schema(tmp_path: Path) -> None:
    evidence = MODULE.validate_scope(
        write_consumer_state(tmp_path),
        "tigrbl-memdedupe-engine-demo",
        "cert.tigrbl-memdedupe-engine-demo",
    )

    assert evidence["provider"] == "letsencrypt"
    assert evidence["domain_names"] == [
        "memdedupe.engine-demo.tigrbl.dev",
        "dedupe.engine-demo.tigrbl.dev",
    ]


@pytest.mark.parametrize(
    ("certificate", "expected"),
    [
        ({"certificate_type": "letsencrypt", "provider": "other"}, "letsencrypt"),
        ({"provider": "letsencrypt", "api_payload": {"provider": "other"}}, "letsencrypt"),
        ({"api_payload": {"provider": "letsencrypt"}}, "letsencrypt"),
    ],
)
def test_provider_precedence(certificate: dict, expected: str) -> None:
    assert MODULE.certificate_provider(certificate) == expected


def test_rejects_non_letsencrypt_provider(tmp_path: Path) -> None:
    document = yaml.safe_load(ACTUAL_CONSUMER_SCHEMA)
    certificate = document["spec"]["certificates"][0]
    certificate["certificate_type"] = "custom"

    with pytest.raises(ValueError, match="only letsencrypt"):
        MODULE.validate_scope(
            write_consumer_state(tmp_path, yaml.safe_dump(document)),
            "tigrbl-memdedupe-engine-demo",
            "cert.tigrbl-memdedupe-engine-demo",
        )
