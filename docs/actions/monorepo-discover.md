# Monorepo Discover

`actions/monorepo-discover` discovers package cells from configured directory globs and can restrict the result to changed packages.

## Purpose

- Generate package cell JSON for reusable matrix workflows.
- Support generic, uv/Python, and pnpm/Node monorepo layouts.
- Filter package cells by changed files when desired.

## Reusable Workflows

- `.github/workflows/reusable-monorepo-discover.yml`
- `.github/workflows/reusable-monorepo-matrix.yml`

## Example

```yaml
jobs:
  matrix:
    uses: cobycloud/actions/.github/workflows/reusable-monorepo-matrix.yml@main
    with:
      ecosystem: uv
      package-globs: |
        pkgs/*/*
        packages/*
```
