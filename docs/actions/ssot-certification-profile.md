# SSOT Certification Profile

`actions/ssot-certification-profile` runs one SSOT certification profile and uploads profile evidence.

## Purpose

- Verify one profile ID.
- Optionally bind certification to a boundary ID.
- Fail closed by default.

## Reusable Workflow

- `.github/workflows/reusable-ssot-certification-matrix.yml`

## Example

```yaml
jobs:
  certification:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-certification-matrix.yml@main
    with:
      profile-ids: '["profile:core","profile:release"]'
      boundary-id: boundary:current
```
