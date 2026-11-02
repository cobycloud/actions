import re
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
    shared_ref = "279d961ee3d01c42ed019e9fbb6f883af44d854f"
    assert text.count(f"ref: {shared_ref}") == 2
    assert re.fullmatch(r"[0-9a-f]{40}", shared_ref)
    assert "ref: ${{ github.workflow_sha }}" not in text
    assert text.count("persist-credentials: false") >= 2
    assert text.count("./.cobycloud-actions/actions/wyrmctl-setup") == 2


def test_vm104_workflow_materializes_portwyrm_runtime_context() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("Resolve Portwyrm runtime context") == 2
    assert text.count('eq .Destination "/etc/letsencrypt"') == 2
    assert text.count('echo "PUBLIC_HOST=$REQUESTED_PUBLIC_HOST" >> "$GITHUB_ENV"') == 2
    assert text.count('echo "PORTWYRM_CERT_PATH=$cert_path" >> "$GITHUB_ENV"') == 2


def test_vm104_workflow_validates_tls_coverage_before_plan_and_apply() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("actions/wyrmctl-tls-coverage") == 3
    assert text.count("desired-state: ${{ inputs.desired-state }}") == 4
    assert text.count("public-host: ${{ inputs.public-host }}") == 3
    assert 'verify-live: "true"' in text


def test_vm104_workflow_verifies_strict_https_and_served_san() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "--proto '=https' --tlsv1.2" in text
    assert "--insecure" not in text
    assert " -k " not in text
    assert 'grep -Fq "DNS:$PUBLIC_HOST"' in text


def test_vm104_workflow_collects_container_diagnostics_on_failure() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Collect container diagnostics" in text
    assert 'docker inspect "$container"' in text
    assert 'docker logs --tail 300 "$container"' in text
