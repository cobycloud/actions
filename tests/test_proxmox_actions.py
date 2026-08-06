from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProxmoxActionTests(unittest.TestCase):
    def test_typed_actions_require_ca_files(self) -> None:
        for name in ("proxmox-api", "proxmox-task-wait", "proxmox-power"):
            text = (ROOT / "actions" / name / "action.yml").read_text(encoding="utf-8")
            self.assertIn("ca-file", text)
            self.assertNotIn("--insecure", text)

    def test_power_action_has_closed_action_set(self) -> None:
        text = (ROOT / "actions/proxmox-power/action.yml").read_text(encoding="utf-8")
        self.assertIn("start|shutdown", text)
        self.assertIn("allow-hard-stop", text)
        self.assertIn("unsupported power action", text)

    def test_apply_requires_plan_provenance(self) -> None:
        text = (ROOT / "actions/terraform-apply/action.yml").read_text(encoding="utf-8")
        self.assertIn("expected-source-sha", text)
        self.assertIn("expected-plan-sha256", text)
        self.assertIn("plan-run-id", text)
        self.assertIn("sha256sum --check --strict", text)


if __name__ == "__main__":
    unittest.main()
