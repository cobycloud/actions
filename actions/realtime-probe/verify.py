from __future__ import annotations

import argparse
import asyncio
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from websockets.asyncio.client import connect


@dataclass(frozen=True)
class Probe:
    name: str
    url: str
    subprotocols: tuple[str, ...]
    request: dict[str, Any] | None
    expect: dict[str, Any] | None


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def parse_probes(raw: str) -> list[Probe]:
    payload = json.loads(raw)
    if not isinstance(payload, list) or not payload:
        raise ValueError("probes-json must be a non-empty JSON array")

    probes: list[Probe] = []
    names: set[str] = set()
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"probe {index} must be an object")
        name = _require_text(item.get("name"), f"probe {index} name")
        if name in names:
            raise ValueError(f"duplicate probe name: {name}")
        names.add(name)

        url = _require_text(item.get("url"), f"probe {name} url")
        parsed = urlsplit(url)
        if parsed.scheme != "wss" or not parsed.hostname:
            raise ValueError(f"probe {name} url must use wss:// with a hostname")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError(
                f"probe {name} url must not contain credentials, query parameters, or fragments"
            )

        raw_subprotocols = item.get("subprotocols", [])
        if not isinstance(raw_subprotocols, list) or not all(
            isinstance(value, str) and value for value in raw_subprotocols
        ):
            raise ValueError(f"probe {name} subprotocols must be an array of strings")

        request = item.get("request")
        expect = item.get("expect")
        if request is not None and not isinstance(request, dict):
            raise ValueError(f"probe {name} request must be an object")
        if expect is not None and not isinstance(expect, dict):
            raise ValueError(f"probe {name} expect must be an object")
        if expect is not None and request is None:
            raise ValueError(f"probe {name} expect requires request")

        probes.append(
            Probe(
                name=name,
                url=url,
                subprotocols=tuple(raw_subprotocols),
                request=request,
                expect=expect,
            )
        )
    return probes


def _assert_subset(actual: Any, expected: Any, path: str = "response") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path} must be an object")
        for key, expected_value in expected.items():
            if key not in actual:
                raise AssertionError(f"{path}.{key} is missing")
            _assert_subset(actual[key], expected_value, f"{path}.{key}")
        return
    if isinstance(expected, list):
        if actual != expected:
            raise AssertionError(f"{path} does not match the expected array")
        return
    if actual != expected:
        raise AssertionError(f"{path} expected {expected!r}, received {actual!r}")


async def run_probe(probe: Probe, timeout_seconds: float) -> dict[str, Any]:
    started = time.monotonic()
    result: dict[str, Any] = {
        "name": probe.name,
        "url": probe.url,
        "status": "failed",
        "selected_subprotocol": None,
        "response_received": False,
    }
    try:
        async with connect(
            probe.url,
            subprotocols=list(probe.subprotocols) or None,
            open_timeout=timeout_seconds,
            close_timeout=timeout_seconds,
        ) as websocket:
            result["selected_subprotocol"] = websocket.subprotocol
            if probe.subprotocols and websocket.subprotocol not in probe.subprotocols:
                raise AssertionError(
                    "server did not negotiate one of the requested WebSocket subprotocols"
                )
            if probe.request is not None:
                await websocket.send(json.dumps(probe.request, separators=(",", ":")))
                raw_response = await asyncio.wait_for(websocket.recv(), timeout_seconds)
                if not isinstance(raw_response, str):
                    raise AssertionError("expected a JSON text response")
                response = json.loads(raw_response)
                result["response_received"] = True
                if probe.expect is not None:
                    _assert_subset(response, probe.expect)
            result["status"] = "passed"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["elapsed_ms"] = round((time.monotonic() - started) * 1000)
    return result


async def run(probes: list[Probe], timeout_seconds: float) -> list[dict[str, Any]]:
    return await asyncio.gather(
        *(run_probe(probe, timeout_seconds) for probe in probes)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probes-json", required=True)
    parser.add_argument("--evidence-out", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        raise SystemExit("timeout-seconds must be greater than zero")

    probes = parse_probes(args.probes_json)
    results = asyncio.run(run(probes, args.timeout_seconds))
    report = {
        "schema_version": 1,
        "status": "passed" if all(item["status"] == "passed" for item in results) else "failed",
        "probes": results,
    }
    args.evidence_out.parent.mkdir(parents=True, exist_ok=True)
    args.evidence_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
