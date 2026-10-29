# Host Mutation Lock

Composite action: `cobycloud/actions/actions/host-mutation-lock@<immutable-sha>`

Creates a host-local lease that serializes mutating jobs across repositories sharing the same
self-hosted machine. GitHub `concurrency` remains useful inside one repository, but it cannot
coordinate unrelated repositories; this lease supplies that missing host boundary.

## Usage

Acquire immediately before the first host mutation and release from an `always()` step:

```yaml
- name: Acquire VM104 mutation lease
  uses: cobycloud/actions/actions/host-mutation-lock@<immutable-sha>
  with:
    operation: acquire
    lock-name: vm104
    timeout-seconds: "1800"
    stale-seconds: "7200"

- name: Deploy reviewed workload
  run: docker compose up -d --remove-orphans

- name: Apply reviewed Portwyrm plan
  uses: cobycloud/actions/actions/wyrmctl-apply@<immutable-sha>
  with:
    # caller-owned inputs

- name: Release VM104 mutation lease
  if: ${{ always() }}
  uses: cobycloud/actions/actions/host-mutation-lock@<immutable-sha>
  with:
    operation: release
    lock-name: vm104
```

The default owner token combines repository, run ID, run attempt, and job. Acquisition is
idempotent for that job. Release refuses to remove another job's lease. A lease left behind by a
terminated runner may be recovered only after `stale-seconds`.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `operation` | required | `acquire` or `release`. |
| `lock-name` | required | Stable host lane such as `vm102`, `vm103`, or `vm104`. |
| `timeout-seconds` | `1800` | Maximum acquisition wait. |
| `stale-seconds` | `7200` | Minimum age before abandoned-lease recovery. |
| `poll-seconds` | `2` | Acquisition polling interval. |
| `lock-root` | `/tmp/cobycloud-actions-host-locks` | Host-local path shared by all runner services. |
| `owner-token` | derived | Optional caller-supplied owner identity. |

## Operational contract

- All runner services for one VM must share the same host filesystem and `lock-root`.
- Every mutating workflow on that VM must use the same `lock-name`.
- Plan, build, and test jobs do not need the lock; acquire only for apply/deploy/stop/destroy.
- Keep the release step in the same job and guard it with `always()`.
- Set `stale-seconds` longer than the maximum legitimate mutation duration.

