# Monorepo Artifact Join

`actions/monorepo-artifact-join` downloads matrix artifacts, verifies the collected set, and uploads a merged artifact.

## Purpose

- Join artifacts emitted by package matrix jobs.
- Enforce a minimum expected artifact count.
- Produce one aggregate artifact for release, signing, attestation, or publication.

## Reusable Workflow

- `.github/workflows/reusable-monorepo-artifact-join.yml`

## Example

```yaml
jobs:
  join:
    uses: cobycloud/actions/.github/workflows/reusable-monorepo-artifact-join.yml@main
    with:
      artifact-pattern: uv-*
      expected-count: "3"
```
