# Realtime WebSocket Probe

`actions/realtime-probe` verifies public `wss://` endpoints after deployment. It
fails on HTTP errors, failed upgrades, TLS validation errors, unexpected
subprotocol negotiation, timeouts, or optional JSON-response mismatches.

The action accepts a non-empty JSON array. A handshake-only probe is sufficient
to detect a broken reverse-proxy route:

```yaml
- uses: ./.cobycloud-actions/actions/realtime-probe
  with:
    probes-json: >-
      [{"name":"memlru","url":"wss://memlru.engine-demo.tigrbl.dev/ws/lru","subprotocols":["jsonrpc"]}]
```

An optional `request` and expected JSON subset turns the check into an
application-level proof:

```json
{
  "name": "thread-list",
  "url": "wss://example.test/ws/realtime",
  "subprotocols": ["jsonrpc"],
  "request": {"jsonrpc": "2.0", "method": "Thread.list", "params": {}, "id": "deploy-proof"},
  "expect": {"jsonrpc": "2.0", "id": "deploy-proof"}
}
```

Probe URLs must not contain credentials, query strings, or fragments. The
evidence report records endpoint, outcome, negotiated subprotocol, elapsed time,
and redacted failure details; it does not persist request or response payloads.
