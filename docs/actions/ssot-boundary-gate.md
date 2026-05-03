# SSOT Boundary Gate

`actions/ssot-boundary-gate` validates SSOT boundary scope, freeze state, and release readiness.

## Purpose

- Gate work on a specific boundary ID.
- Require frozen scope by default.
- Fail closed when readiness cannot be proven.

## Reusable Workflow

- `.github/workflows/reusable-ssot-boundary-gate.yml`

## Example

```yaml
jobs:
  boundary:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-boundary-gate.yml@main
    with:
      boundary-id: boundary:current
      require-frozen: true
```
