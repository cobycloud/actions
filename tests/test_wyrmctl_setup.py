from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION = ROOT / "actions" / "wyrmctl-setup" / "action.yml"


def test_wyrmctl_setup_defaults_to_certificate_convergence_release() -> None:
    text = ACTION.read_text(encoding="utf-8")

    assert 'default: "0.4.8"' in text
    assert 'WYRMCTL_VERSION: ${{ inputs.version }}' in text
    assert '"wyrmctl==$WYRMCTL_VERSION"' in text
