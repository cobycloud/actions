# Changed Files

`actions/changed-files` detects changed files and derives changed package/app cells from configured monorepo roots.

## Purpose

- Produce changed-file JSON for downstream jobs.
- Produce package-cell JSON for uv, pnpm, or generic monorepo matrices.
- Support configurable package/app globs.

## Reusable Workflow

- `.github/workflows/reusable-changed-files.yml`

## Example

```yaml
jobs:
  changed:
    uses: cobycloud/actions/.github/workflows/reusable-changed-files.yml@main
    with:
      ecosystem: pnpm
      package-globs: |
        apps/*
        packages/*
```
