from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / "actions/wyrmctl-plan/action.yml"
MODULE_PATH = ROOT / "actions/wyrmctl-plan/validate_plan_artifact.py"
SPEC = importlib.util.spec_from_file_location("validate_plan_artifact", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def artifact(*, operations=None, conflicts=None, dns_conflicts=None) -> dict:
    return {
        "apiVersion": "wyrmctl.com/v1",
        "kind": "PlanArtifact",
        "schemaVersion": 1,
        "spec": {
            "operations": [] if operations is None else operations,
            "conflicts": [] if conflicts is None else conflicts,
            "dns": {"conflicts": [] if dns_conflicts is None else dns_conflicts},
        },
    }


def test_owned_update_plan_is_conflict_free() -> None:
    MODULE.require_conflict_free(
        artifact(
            operations=[
                {
                    "action": "update",
                    "kind": "proxy_host",
                    "resource_id": "proxy.demo",
                }
            ]
        )
    )


def test_unmanaged_conflict_plan_is_rejected() -> None:
    with pytest.raises(ValueError, match="unmanaged_resource"):
        MODULE.require_conflict_free(
            artifact(conflicts=[{"code": "unmanaged_resource", "message": "adopt first"}])
        )


def test_dns_conflict_plan_is_rejected() -> None:
    with pytest.raises(ValueError, match="read_only_dns_provider"):
        MODULE.require_conflict_free(
            artifact(dns_conflicts=[{"code": "read_only_dns_provider"}])
        )


def test_malformed_conflict_collection_is_rejected() -> None:
    with pytest.raises(ValueError, match="spec.conflicts must be an array"):
        MODULE.require_conflict_free(artifact(conflicts={"code": "bad"}))


def test_action_only_tolerates_exit_one_after_strict_conflict_free_inspection() -> None:
    text = ACTION.read_text(encoding="utf-8")

    assert "set +e" in text
    assert "plan_exit=$?" in text
    assert 'if [[ ! -s "$ARTIFACT_OUT" ]]' in text
    strict = 'artifact inspect "$ARTIFACT_OUT" --strict'
    conflict_free = 'validate_plan_artifact.py" "$ARTIFACT_OUT"'
    allowed_exit = 'case "$plan_exit" in'
    assert text.index(strict) < text.index(conflict_free) < text.index(allowed_exit)
    assert "Wyrmctl plan failed with unsupported exit code" in text
