# SSOT Sync Statuses

`actions/ssot-sync-statuses` synchronizes SSOT implementation status from evidence or target repository truth.

## Purpose

- Run governed status synchronization.
- Support evidence-path based sync.
- Optionally fail when sync mutates tracked files.

## Reusable Workflow

- `.github/workflows/reusable-ssot-sync-statuses.yml`

## Example

```yaml
jobs:
  sync:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-sync-statuses.yml@main
    with:
      evidence-path: evidence
      fail-on-changes: true
```
