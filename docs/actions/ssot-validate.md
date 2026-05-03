# SSOT Validate

`actions/ssot-validate` validates an SSOT registry and optionally uploads validation reports.

## Purpose

- Run a standard SSOT validation gate.
- Keep registry path explicit.
- Support caller-specific validation command overrides.

## Reusable Workflow

- `.github/workflows/reusable-ssot-validate.yml`

## Example

```yaml
jobs:
  ssot:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-validate.yml@main
    with:
      registry-path: .ssot/registry.json
      report-path: reports/ssot-validation.json
```
