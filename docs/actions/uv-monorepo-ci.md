# uv Monorepo CI

`actions/uv-monorepo-ci` runs one uv/Python monorepo package cell.

## Purpose

- Set up Python and uv.
- Compute monorepo `PYTHONPATH`.
- Run install, compile, test, docs, and build commands for a package path.

## Reusable Workflow

- `.github/workflows/reusable-uv-monorepo-ci.yml`

## Example

```yaml
jobs:
  uv:
    uses: cobycloud/actions/.github/workflows/reusable-uv-monorepo-ci.yml@main
    with:
      package-cells: '[{"name":"core","path":"pkgs/core/example","ecosystem":"uv"}]'
```
