from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github/workflows/reusable-vm104-wyrmctl-certificate-adopt.yml"


def _workflow() -> tuple[dict, str]:
    text = WORKFLOW.read_text(encoding="utf-8")
    return yaml.safe_load(text), text


def test_adoption_workflow_is_owner_and_resource_scoped() -> None:
    workflow, text = _workflow()
    inputs = workflow[True]["workflow_call"]["inputs"]

    assert set(inputs) == {
        "desired-state",
        "owner",
        "certificate-resource-id",
        "confirmation",
    }
    assert all(item["required"] is True for item in inputs.values())
    assert 'test "$CONFIRMATION" = "ADOPT $CERTIFICATE_RESOURCE_ID"' in text
    assert "requires exactly one desired certificate" in text
    assert 'metadata.get("owner") != expected_owner' in text
    assert 'metadata.get("resource_id") != expected_resource_id' in text
    assert 'metadata.get("managed_by") != "wyrmctl"' in text


def test_adoption_workflow_is_vm104_protected_and_metadata_only() -> None:
    workflow, text = _workflow()
    job = workflow["jobs"]["adopt"]

    assert job["runs-on"]["group"] == "portwyrm-deployment"
    assert "vm104" in job["runs-on"]["labels"]
    assert job["environment"] == "deployment"
    assert workflow["permissions"] == {"contents": "read"}
    assert "--only certificates" in text
    assert "--metadata-only" in text
    assert "--certificate-mode reuse" in text
    assert "--prune-owned" not in text
    assert "--force" not in text
    assert "--allow-field-drift" not in text


def test_adoption_workflow_masks_credentials_and_uploads_evidence() -> None:
    _, text = _workflow()

    assert "PORTWYRM_WYRMCTL_SECRET_B64" in text
    assert 'echo "::add-mask::$secret"' in text
    assert "adoption-scope.json" in text
    assert "adoption-result.json" in text
    assert "execution-binding.json" in text
    assert "sha256sums.txt" in text
    assert "actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9" in text


def test_adoption_workflow_uses_immutable_action_pins() -> None:
    _, text = _workflow()

    assert "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803" in text
    assert (
        "cobycloud/actions/actions/wyrmctl-setup@"
        "1f67ac678f115a88f69e5ed8b149a70ab6c374b3"
    ) in text
    assert "@master" not in text
    assert "@main" not in text
