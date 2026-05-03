# Node Lint Typecheck

`actions/node-lint-typecheck` installs Node dependencies and runs the common JavaScript package validation sequence for one matrix cell.

## Purpose

- Install a caller-selected Node.js version.
- Run dependency installation.
- Run lint, typecheck, test, and build commands.
- Support package subdirectories in monorepos.

## Dependencies

- `actions/setup-node`
- npm, pnpm, or yarn through caller-provided commands

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `node-version` | `20` | Node.js version to install. |
| `working-directory` | `.` | Directory containing `package.json`. |
| `install-command` | `npm ci` | Dependency install command. |
| `lint-command` | `npm run lint --if-present` | Lint gate. |
| `typecheck-command` | `npm run typecheck --if-present` | Typecheck gate. |
| `test-command` | `npm test --if-present` | Test gate. |
| `build-command` | `npm run build --if-present` | Build gate. |
| `cache` | `npm` | Cache mode for `actions/setup-node`. |
| `cache-dependency-path` | `package-lock.json` | Cache dependency file relative to `working-directory`. |

## Reusable Workflows

- `.github/workflows/reusable-node-lint-typecheck.yml`
- `.github/workflows/reusable-node-version-matrix.yml`
- `.github/workflows/reusable-cross-platform-node.yml`
- `.github/workflows/reusable-os-matrix.yml`

## Example

```yaml
jobs:
  node:
    uses: cobycloud/actions/.github/workflows/reusable-node-version-matrix.yml@main
    with:
      node-versions: '["18","20","22"]'
      working-directory: apps/client
```
