from __future__ import annotations

import json
import unittest

from verify import _assert_subset, parse_probes


class ParseProbesTests(unittest.TestCase):
    def test_accepts_secure_handshake_probe(self) -> None:
        probes = parse_probes(
            json.dumps(
                [
                    {
                        "name": "lru",
                        "url": "wss://memlru.engine-demo.tigrbl.dev/ws/lru",
                        "subprotocols": ["jsonrpc"],
                    }
                ]
            )
        )
        self.assertEqual(probes[0].subprotocols, ("jsonrpc",))

    def test_rejects_insecure_or_secret_bearing_url(self) -> None:
        for url in (
            "ws://example.test/ws",
            "wss://user:secret@example.test/ws",
            "wss://example.test/ws?token=secret",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                parse_probes(json.dumps([{"name": "bad", "url": url}]))

    def test_expect_requires_request(self) -> None:
        with self.assertRaisesRegex(ValueError, "expect requires request"):
            parse_probes(
                json.dumps(
                    [
                        {
                            "name": "bad",
                            "url": "wss://example.test/ws",
                            "expect": {"jsonrpc": "2.0"},
                        }
                    ]
                )
            )


class SubsetTests(unittest.TestCase):
    def test_nested_subset(self) -> None:
        _assert_subset(
            {"jsonrpc": "2.0", "result": {"ok": True, "count": 1}},
            {"result": {"ok": True}},
        )

    def test_mismatch_fails(self) -> None:
        with self.assertRaisesRegex(AssertionError, "response.result.ok"):
            _assert_subset({"result": {"ok": False}}, {"result": {"ok": True}})


if __name__ == "__main__":
    unittest.main()
