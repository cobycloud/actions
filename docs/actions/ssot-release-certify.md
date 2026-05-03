# SSOT Release Certify

`actions/ssot-release-certify` certifies, promotes, or publishes an SSOT release entity.

## Purpose

- Run release operations against a specific release ID.
- Support `certify`, `promote`, and `publish` operations.
- Preserve optional release evidence artifacts.

## Reusable Workflow

- `.github/workflows/reusable-ssot-release-certify.yml`

## Example

```yaml
jobs:
  certify:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-release-certify.yml@main
    with:
      release-id: release:2026-05
      operation: certify
      fail-closed: true
```
