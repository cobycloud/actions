from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/reusable-vm104-portwyrm-certificate-renew.yml"


def test_renewal_is_confirmation_gated_and_owner_scoped() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'test "$CONFIRMATION" = "RENEW $CERTIFICATE_RESOURCE_ID"' in text
    assert "actions/portwyrm-certificate-renew/validate_scope.py" in text
    assert "not domain_sets_match(expected_domains, live_domains)" in text
    assert "not domain_sets_match(expected_domains, renewed.get(\"domain_names\"))" in text
    assert 'environment: deployment' in text


def test_preflight_artifact_upload_does_not_mask_validation_failure() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "if-no-files-found: warn" in text


def test_renewal_uses_portwyrm_force_reissue_without_deletion() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'f"{base_url}/nginx/certificates/{live[\'id\']}/renew"' in text
    assert 'params={"force": "true"}' in text
    assert "session.delete(" not in text
    assert "/nginx/certificates/{live['id']}" not in text.replace(
        "/nginx/certificates/{live['id']}/renew", ""
    )


def test_renewal_holds_host_lock_and_strictly_verifies_live_tls() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert text.count("actions/host-mutation-lock") == 2
    assert "operation: acquire" in text
    assert "operation: release" in text
    assert "ssl.create_default_context()" in text
    assert "server_hostname=hostname" in text
    assert "getpeercert(binary_form=True)" in text
    assert "len(set(fingerprints.values())) != 1" in text
    assert "--insecure" not in text


def test_renewal_checks_out_an_immutable_shared_action_revision() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    shared_ref = "031225e62b8716b47f3439829497e397e0e93a5e"
    assert f"ref: {shared_ref}" in text
    assert "persist-credentials: false" in text
