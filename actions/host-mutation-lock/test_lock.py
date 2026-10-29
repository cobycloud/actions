from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("lock.py")


def load_lock_module():
    spec = importlib.util.spec_from_file_location("host_mutation_lock", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load host mutation lock module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HostMutationLockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.lock_root = Path(self.temp_dir.name) / "locks"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_lock(self, operation: str, owner: str, *, expect: int = 0) -> None:
        environment = os.environ | {
            "LOCK_OPERATION": operation,
            "LOCK_NAME": "vm104",
            "LOCK_ROOT": str(self.lock_root),
            "LOCK_TIMEOUT_SECONDS": "0",
            "LOCK_STALE_SECONDS": "60",
            "LOCK_POLL_SECONDS": "1",
            "LOCK_OWNER_TOKEN": owner,
        }
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=False,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)

    def test_owner_safe_lifecycle(self) -> None:
        self.run_lock("acquire", "owner-a")
        self.run_lock("acquire", "owner-a")
        self.run_lock("acquire", "owner-b", expect=1)
        self.run_lock("release", "owner-b", expect=1)
        self.run_lock("release", "owner-a")
        self.run_lock("acquire", "owner-b")
        self.run_lock("release", "owner-b")

    def test_recovers_stale_lease(self) -> None:
        lock_path = self.lock_root / "vm104.lock"
        lock_path.mkdir(parents=True)
        (lock_path / "owner-token").write_text("owner-stale\n", encoding="utf-8")
        (lock_path / "acquired-at").write_text("1\n", encoding="utf-8")
        self.run_lock("acquire", "owner-new")
        self.run_lock("release", "owner-new")
        self.assertFalse(lock_path.exists())

    def test_active_timestamp_is_not_recovered(self) -> None:
        lock_path = self.lock_root / "vm104.lock"
        lock_path.mkdir(parents=True)
        (lock_path / "owner-token").write_text("owner-active\n", encoding="utf-8")
        (lock_path / "acquired-at").write_text(f"{int(time.time())}\n", encoding="utf-8")
        self.run_lock("acquire", "owner-new", expect=1)

    def test_termination_releases_lease_won_during_cancellation(self) -> None:
        module = load_lock_module()
        lock_path = self.lock_root / "vm104.lock"
        lock_path.mkdir(parents=True)
        (lock_path / "owner-token").write_text("cancelled-owner\n", encoding="utf-8")
        (lock_path / "acquired-at").write_text(
            f"{int(time.time())}\n", encoding="utf-8"
        )
        module._OWNED_LOCK_PATH = lock_path
        module._OWNED_TOKEN = "cancelled-owner"

        module.handle_termination(15, None)

        self.assertTrue(module._INTERRUPTED)
        self.assertFalse(lock_path.exists())


if __name__ == "__main__":
    unittest.main()

