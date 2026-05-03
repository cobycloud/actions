# pnpm Monorepo CI

`actions/pnpm-monorepo-ci` runs one pnpm/Node monorepo package cell.

## Purpose

- Set up pnpm and Node.
- Run package-level install, lint, typecheck, test, and build commands.
- Support pnpm workspaces and package-directory validation.

## Reusable Workflow

- `.github/workflows/reusable-pnpm-monorepo-ci.yml`

## Example

```yaml
jobs:
  pnpm:
    uses: cobycloud/actions/.github/workflows/reusable-pnpm-monorepo-ci.yml@main
    with:
      package-cells: '[{"name":"client","path":"apps/client","ecosystem":"pnpm"}]'
```
