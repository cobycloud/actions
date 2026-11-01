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
    assert 'env-file: {type: string, required: false, default: ""}' in text
    assert 'test -r "$ENV_FILE"' in text


def test_vm104_workflow_preserves_reviewed_plan_boundary() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "sha256sum deployment-evidence/wyrmctl-plan.json" in text
    assert "sha256sum --check deployment-evidence/plan.sha256" in text
    assert "./.cobycloud-actions/actions/wyrmctl-plan" in text
    assert "./.cobycloud-actions/actions/wyrmctl-apply" in text
    assert "./.cobycloud-actions/actions/host-mutation-lock" in text


def test_vm104_workflow_checks_out_shared_actions_before_local_use() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("repository: cobycloud/actions") == 2
    assert text.count("path: .cobycloud-actions") == 2
    assert text.count("persist-credentials: false") >= 2
    assert text.count("./.cobycloud-actions/actions/wyrmctl-setup") == 2


def test_vm104_workflow_materializes_portwyrm_runtime_context() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("Resolve Portwyrm runtime context") == 2
    assert text.count('eq .Destination "/etc/letsencrypt"') == 2
    assert text.count('echo "PUBLIC_HOST=$REQUESTED_PUBLIC_HOST" >> "$GITHUB_ENV"') == 2
    assert text.count('echo "PORTWYRM_CERT_PATH=$cert_path" >> "$GITHUB_ENV"') == 2


def test_vm104_workflow_collects_container_diagnostics_on_failure() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Collect container diagnostics" in text
    assert 'docker inspect "$container"' in text
    assert 'docker logs --tail 300 "$container"' in text
