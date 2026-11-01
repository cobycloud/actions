from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/reusable-vm104-wyrmctl-compose-deploy.yml"


def test_vm104_workflow_enforces_runner_and_network_boundaries() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("group: portwyrm-deployment") == 2
    assert text.count("labels: [self-hosted, Linux, X64, vm104]") == 2
    assert "has(\"private\") and has(\"edge\")" in text
    assert 'lock-name: vm104' in text
    assert "PORTWYRM_NETWORK: portwyrm-edge" in text


def test_vm104_workflow_preserves_reviewed_plan_boundary() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "sha256sum deployment-evidence/wyrmctl-plan.json" in text
    assert "sha256sum --check deployment-evidence/plan.sha256" in text
    assert "./actions/wyrmctl-plan" in text
    assert "./actions/wyrmctl-apply" in text
    assert "./actions/host-mutation-lock" in text
