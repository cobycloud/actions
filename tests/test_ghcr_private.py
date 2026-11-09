"""Execute the private publication boundary check with registry responses mocked."""
import io
import json
import os
from pathlib import Path
import subprocess
import textwrap
import unittest
from unittest.mock import patch


WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/reusable-ghcr-publish.yml'


class PrivatePublication(unittest.TestCase):
    def verify(self, visibility='private', anonymous_code=1, error='unauthorized'):
        source = WORKFLOW.read_text().split('      - name: Verify private package and pull boundaries', 1)[1]
        source = source.split('        run: |\n', 1)[1].split('\n      - name:', 1)[0]
        calls = []

        def run(args, **kwargs):
            calls.append(args)
            if '--config' in args:
                return subprocess.CompletedProcess(args, anonymous_code, '', error)
            return subprocess.CompletedProcess(args, 0)

        with patch.dict(os.environ, {'IMAGE': 'ghcr.io/groupsum/envelope-relay-api', 'DIGEST': 'sha256:abc',
                                     'GITHUB_API_URL': 'https://api.github.com', 'GH_TOKEN': 'fixture'}), \
                patch('urllib.request.urlopen', return_value=io.StringIO(json.dumps({'visibility': visibility}))), \
                patch('subprocess.run', side_effect=run):
            exec(compile(textwrap.dedent(source), 'private-check', 'exec'), {})
        return calls

    def test_private_requires_authenticated_pull(self):
        calls = self.verify()
        self.assertEqual(len(calls), 2)
        self.assertIn('--config', calls[0])
        self.assertEqual(calls[1], ['docker', 'pull', 'ghcr.io/groupsum/envelope-relay-api@sha256:abc'])

    def test_public_package_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, 'Expected a private'):
            self.verify(visibility='public')

    def test_anonymous_access_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, 'unexpectedly allowed'):
            self.verify(anonymous_code=0)

    def test_network_failure_is_not_private_access_evidence(self):
        with self.assertRaisesRegex(SystemExit, 'without an authentication denial'):
            self.verify(error='connection timed out')

    def test_public_is_the_compatible_default(self):
        workflow = WORKFLOW.read_text()
        self.assertIn("if: inputs.visibility == 'public'", workflow)
        self.assertIn("if: inputs.visibility == 'private'", workflow)
        self.assertIn('default: public', workflow)

    def test_private_provenance_does_not_depend_on_paid_github_attestations(self):
        workflow = WORKFLOW.read_text()
        public = workflow.split('      - name: Attest immutable GHCR provenance', 1)[1]
        self.assertTrue(public.lstrip().startswith("if: inputs.visibility == 'public'"))
        self.assertIn(".get('buildx.build.provenance')", workflow)
        self.assertIn("'cosign', 'attest'", workflow)
        self.assertIn("'cosign', 'verify-attestation'", workflow)


if __name__ == '__main__':
    unittest.main()
