from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "actions/wyrmctl-tls-coverage/validate.py"
SPEC = importlib.util.spec_from_file_location("wyrmctl_tls_coverage", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def desired_state(*, proxy_domains: list[str], certificate_domains: list[str]) -> dict:
    return {
        "spec": {
            "proxyHosts": [
                {
                    "domain_names": proxy_domains,
                    "certificate_ref": "cert.demo",
                }
            ],
            "certificates": [
                {
                    "domain_names": certificate_domains,
                    "meta": {"resource_id": "cert.demo"},
                }
            ],
        }
    }


def test_accepts_exact_certificate_coverage_for_all_proxy_domains() -> None:
    MODULE.validate_document(
        desired_state(
            proxy_domains=["demo.tigrbl.dev", "legacy.tigrbl.dev"],
            certificate_domains=["demo.tigrbl.dev", "legacy.tigrbl.dev"],
        ),
        "demo.tigrbl.dev",
    )


def test_accepts_single_label_wildcard_coverage() -> None:
    MODULE.validate_document(
        desired_state(
            proxy_domains=["demo.engine-demo.tigrbl.dev"],
            certificate_domains=["*.engine-demo.tigrbl.dev"],
        ),
        "demo.engine-demo.tigrbl.dev",
    )


def test_rejects_certificate_that_does_not_cover_proxy_alias() -> None:
    with pytest.raises(ValueError, match="does not cover.*legacy"):
        MODULE.validate_document(
            desired_state(
                proxy_domains=["demo.tigrbl.dev", "legacy.tigrbl.dev"],
                certificate_domains=["demo.tigrbl.dev"],
            ),
            "demo.tigrbl.dev",
        )


def test_rejects_deep_hostname_for_single_label_wildcard() -> None:
    with pytest.raises(ValueError, match="does not cover"):
        MODULE.validate_document(
            desired_state(
                proxy_domains=["deep.demo.engine-demo.tigrbl.dev"],
                certificate_domains=["*.engine-demo.tigrbl.dev"],
            ),
            "deep.demo.engine-demo.tigrbl.dev",
        )


def test_rejects_public_host_not_declared_by_proxy() -> None:
    with pytest.raises(ValueError, match="is not declared"):
        MODULE.validate_document(
            desired_state(
                proxy_domains=["demo.tigrbl.dev"],
                certificate_domains=["demo.tigrbl.dev"],
            ),
            "other.tigrbl.dev",
        )


def test_rejects_unknown_certificate_reference() -> None:
    document = desired_state(
        proxy_domains=["demo.tigrbl.dev"],
        certificate_domains=["demo.tigrbl.dev"],
    )
    document["spec"]["proxyHosts"][0]["certificate_ref"] = "cert.missing"
    with pytest.raises(ValueError, match="unknown certificate"):
        MODULE.validate_document(document, "demo.tigrbl.dev")


def test_live_verification_checks_every_domain_bound_to_one_certificate() -> None:
    observed: list[str] = []

    def fetcher(hostname: str, port: int, timeout: float) -> tuple[str, tuple[str, ...]]:
        observed.append(hostname)
        assert port == 443
        assert timeout == 5.0
        return "shared-fingerprint", ("demo.tigrbl.dev", "legacy.tigrbl.dev")

    fingerprints = MODULE.verify_live_bindings(
        {"cert.demo": ("demo.tigrbl.dev", "legacy.tigrbl.dev")},
        timeout=5.0,
        fetcher=fetcher,
    )

    assert observed == ["demo.tigrbl.dev", "legacy.tigrbl.dev"]
    assert fingerprints == {"cert.demo": "shared-fingerprint"}


def test_live_verification_rejects_stale_alias_certificate() -> None:
    def fetcher(hostname: str, _port: int, _timeout: float) -> tuple[str, tuple[str, ...]]:
        return "fingerprint", ("demo.tigrbl.dev",)

    with pytest.raises(ValueError, match="legacy.*does not cover"):
        MODULE.verify_live_bindings(
            {"cert.demo": ("demo.tigrbl.dev", "legacy.tigrbl.dev")},
            fetcher=fetcher,
        )


def test_live_verification_rejects_different_certificates_for_one_reference() -> None:
    def fetcher(hostname: str, _port: int, _timeout: float) -> tuple[str, tuple[str, ...]]:
        return hostname, (hostname,)

    with pytest.raises(ValueError, match="different live certificates"):
        MODULE.verify_live_bindings(
            {"cert.demo": ("demo.tigrbl.dev", "legacy.tigrbl.dev")},
            fetcher=fetcher,
        )
