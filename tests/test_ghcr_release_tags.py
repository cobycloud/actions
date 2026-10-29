"""Exercise the actual inline publisher validation without registry writes."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/reusable-ghcr-publish.yml"


class ReleaseTags(unittest.TestCase):
    def classify(self, tag, pattern=None):
        workflow = WORKFLOW.read_text()
        block = workflow.split("      - name: Validate release tag\n", 1)[1]
        script = block.split("        run: |\n", 1)[1].split("\n      - uses:", 1)[0]
        script = "\n".join(line[10:] for line in script.splitlines())
        default = workflow.split("      tag-regex:", 1)[1].split("default: ", 1)[1].splitlines()[0]
        bash = shutil.which("bash") if os.name != "nt" else r"C:\Program Files\Git\bin\bash.exe"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "outputs"
            env = dict(os.environ, RELEASE_TAG=tag, TAG_REGEX=pattern or default, GITHUB_OUTPUT=output.as_posix())
            result = subprocess.run([bash, "-c", script], env=env, capture_output=True, text=True)
            return result.returncode, output.read_text() if output.exists() else ""

    def test_supported_versions(self):
        for tag, version, stable in [
            ("v0.1.0a22", "0.1.0a22", "false"),
            ("v1.2.3b4", "1.2.3b4", "false"),
            ("v1.2.3rc1", "1.2.3rc1", "false"),
            ("v1.2.3-alpha.2", "1.2.3-alpha.2", "false"),
            ("v1.2.3", "1.2.3", "true"),
            ("v0.0.0", "0.0.0", "true"),
        ]:
            with self.subTest(tag=tag):
                code, output = self.classify(tag)
                self.assertEqual(code, 0)
                self.assertEqual(output, f"version={version}\nstable={stable}\n")

    def test_invalid_refs_are_rejected(self):
        for tag in ["master", "v1.2", "v1.2.3/invalid", "v1.2.3\nlatest=true"]:
            with self.subTest(tag=tag):
                self.assertNotEqual(self.classify(tag)[0], 0)

    def test_custom_validation_cannot_enable_stable_aliases(self):
        self.assertEqual(self.classify("v1.2.3.dev1", ".*")[1], "version=1.2.3.dev1\nstable=false\n")
        self.assertNotEqual(self.classify("v1.2.3/unsafe", ".*")[0], 0)

    def test_metadata_disables_implicit_latest(self):
        workflow = WORKFLOW.read_text()
        self.assertIn("flavor: latest=false", workflow)
        self.assertIn("type=raw,value=${{ steps.release.outputs.version }},priority=1000", workflow)
        aliases = [line for line in workflow.splitlines() if "type=semver" in line or "type=raw,value=latest" in line]
        self.assertEqual(len(aliases), 3)
        for alias in aliases:
            self.assertIn("enable=${{ steps.release.outputs.stable == 'true' }}", alias)


if __name__ == "__main__":
    unittest.main()
