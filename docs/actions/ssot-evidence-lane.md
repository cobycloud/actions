# SSOT Evidence Lane

`actions/ssot-evidence-lane` runs an evidence command and uploads SSOT evidence artifacts.

## Purpose

- Execute one evidence lane.
- Pass registry, boundary, profile, and evidence IDs as environment variables.
- Upload the evidence output path as an artifact.

## Reusable Workflow

- `.github/workflows/reusable-ssot-evidence-lane.yml`

## Example

```yaml
jobs:
  evidence:
    uses: cobycloud/actions/.github/workflows/reusable-ssot-evidence-lane.yml@main
    with:
      evidence-id: evidence:tests
      boundary-id: boundary:current
      evidence-command: uv run pytest --junitxml=evidence/junit.xml
      evidence-path: evidence
```
