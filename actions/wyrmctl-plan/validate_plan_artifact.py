from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _mapping(value: object, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _conflicts(value: object, field: str) -> list[object]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def require_conflict_free(document: object) -> None:
    root = _mapping(document, "artifact")
    spec = _mapping(root.get("spec"), "spec")
    conflicts = _conflicts(spec.get("conflicts"), "spec.conflicts")
    dns_value = spec.get("dns")
    dns = {} if dns_value is None else _mapping(dns_value, "spec.dns")
    dns_conflicts = _conflicts(dns.get("conflicts"), "spec.dns.conflicts")

    if conflicts or dns_conflicts:
        codes = []
        for conflict in [*conflicts, *dns_conflicts]:
            if isinstance(conflict, dict) and conflict.get("code"):
                codes.append(str(conflict["code"]))
            else:
                codes.append("unspecified")
        raise ValueError(
            "plan artifact contains blocking conflict(s): " + ", ".join(codes)
        )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: validate_plan_artifact.py ARTIFACT", file=sys.stderr)
        return 2
    try:
        document = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        require_conflict_free(document)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Unsafe Wyrmctl plan artifact: {exc}", file=sys.stderr)
        return 1
    print("Wyrmctl plan artifact is conflict-free")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
