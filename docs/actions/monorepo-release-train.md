# Monorepo Release Train

`actions/monorepo-release-train` executes one ordered command over package cells.

## Purpose

- Run ordered publish, promote, or version commands across package sets.
- Preserve package order from the provided JSON array.
- Expose `PACKAGE_NAME` and `PACKAGE_PATH` for caller-owned commands.

## Reusable Workflow

- `.github/workflows/reusable-monorepo-release-train.yml`

## Example

```yaml
jobs:
  release:
    uses: cobycloud/actions/.github/workflows/reusable-monorepo-release-train.yml@main
    with:
      package-cells: '[{"name":"core","path":"pkgs/core/example"}]'
      command: uv build
```
