#!/usr/bin/env python3
"""Host-local cross-repository mutation lease for self-hosted runners."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from pathlib import Path


def required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise ValueError(f"{name} is required")
    return value


def integer(name: str, default: int, *, positive: bool = False) -> int:
    raw = os.environ.get(name, str(default))
    if not raw.isdecimal():
        raise ValueError(f"{name} must be a non-negative integer")
    value = int(raw)
    if positive and value == 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def owner_token() -> str:
    configured = os.environ.get("LOCK_OWNER_TOKEN", "")
    if configured:
        return configured
    fields = (
        os.environ.get("GITHUB_REPOSITORY", "local"),
        os.environ.get("GITHUB_RUN_ID", "0"),
        os.environ.get("GITHUB_RUN_ATTEMPT", "0"),
        os.environ.get("GITHUB_JOB", "job"),
    )
    return ":".join(fields)


def emit_output(lock_path: Path, owner: str) -> None:
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"lock-path={lock_path}\nowner-token={owner}\n")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def release(lock_path: Path, owner: str) -> None:
    if not lock_path.exists():
        emit_output(lock_path, owner)
        return
    current_owner = read_text(lock_path / "owner-token")
    if current_owner != owner:
        raise RuntimeError(
            f"refusing to release lease owned by {current_owner or 'unknown'}"
        )
    (lock_path / "owner-token").unlink(missing_ok=True)
    (lock_path / "acquired-at").unlink(missing_ok=True)
    lock_path.rmdir()
    emit_output(lock_path, owner)
    print(f"Released host mutation lease: {lock_path.stem}")


def acquire(
    lock_root: Path,
    lock_path: Path,
    owner: str,
    timeout_seconds: int,
    stale_seconds: int,
    poll_seconds: int,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            lock_path.mkdir()
            (lock_path / "owner-token").write_text(f"{owner}\n", encoding="utf-8")
            (lock_path / "acquired-at").write_text(
                f"{int(time.time())}\n", encoding="utf-8"
            )
            emit_output(lock_path, owner)
            print(f"Acquired host mutation lease: {lock_path.stem}")
            return
        except FileExistsError:
            pass

        current_owner = read_text(lock_path / "owner-token")
        if current_owner == owner:
            emit_output(lock_path, owner)
            print(f"Host mutation lease already owned by this job: {lock_path.stem}")
            return

        acquired_raw = read_text(lock_path / "acquired-at")
        try:
            acquired_at = int(acquired_raw)
        except ValueError:
            acquired_at = int(lock_path.stat().st_mtime)
        now = int(time.time())
        if now - acquired_at >= stale_seconds:
            safe_owner = re.sub(r"[^A-Za-z0-9._-]", "_", owner)
            stale_path = lock_root / f"{lock_path.stem}.stale.{safe_owner}.{now}"
            try:
                lock_path.replace(stale_path)
            except OSError:
                pass
            else:
                shutil.rmtree(stale_path)
                print(f"Recovered abandoned host mutation lease: {lock_path.stem}")
                continue

        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"timed out waiting for lease owned by {current_owner or 'unknown'}"
            )
        time.sleep(poll_seconds)


def main() -> int:
    try:
        operation = required("LOCK_OPERATION")
        lock_name = required("LOCK_NAME")
        if operation not in {"acquire", "release"}:
            raise ValueError("LOCK_OPERATION must be acquire or release")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", lock_name):
            raise ValueError("LOCK_NAME must be a safe host lane identifier")
        timeout_seconds = integer("LOCK_TIMEOUT_SECONDS", 1800)
        stale_seconds = integer("LOCK_STALE_SECONDS", 7200, positive=True)
        poll_seconds = integer("LOCK_POLL_SECONDS", 2, positive=True)
        lock_root = Path(
            os.environ.get("LOCK_ROOT", "/tmp/cobycloud-actions-host-locks")
        ).resolve()
        lock_root.mkdir(parents=True, exist_ok=True, mode=0o700)
        lock_path = lock_root / f"{lock_name}.lock"
        owner = owner_token()
        if operation == "release":
            release(lock_path, owner)
        else:
            acquire(
                lock_root,
                lock_path,
                owner,
                timeout_seconds,
                stale_seconds,
                poll_seconds,
            )
        return 0
    except (OSError, RuntimeError, TimeoutError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

