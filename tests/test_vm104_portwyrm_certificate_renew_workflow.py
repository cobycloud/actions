from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/reusable-vm104-portwyrm-certificate-renew.yml"


def test_renewal_is_confirmation_gated_and_owner_scoped() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'test "$CONFIRMATION" = "RENEW $CERTIFICATE_RESOURCE_ID"' in text
    assert 'item.get("meta", {}).get("owner") == owner' in text
    assert 'item.get("meta", {}).get("resource_id") == resource_id' in text
    assert "live.get(\"domain_names\") != expected_domains" in text
    assert 'environment: deployment' in text


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

    shared_ref = "279d961ee3d01c42ed019e9fbb6f883af44d854f"
    assert f"ref: {shared_ref}" in text
    assert "persist-credentials: false" in text
