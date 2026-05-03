# JavaScript Framework CI

`actions/js-framework-ci` runs frontend checks for Vite, Svelte, Vue, React, and generic Node applications.

## Purpose

- Normalize frontend install, lint, typecheck, test, and build lanes.
- Provide framework presets for common typecheck command names.
- Allow every command to be overridden by the caller.
- Upload built artifacts through the reusable workflow wrapper.

## Dependencies

- `actions/setup-node`
- npm, pnpm, or yarn through caller-provided commands

## Presets

| Framework | Typecheck default |
| --- | --- |
| `svelte` | `npm run check --if-present` |
| `vue` | `npm run type-check --if-present` |
| `react` | `npm run typecheck --if-present` |
| `vite` | `npm run typecheck --if-present` |
| `generic` | `npm run typecheck --if-present` |

## Reusable Workflow

- `.github/workflows/reusable-js-framework-ci.yml`
- `.github/workflows/reusable-js-framework-matrix.yml`
- `.github/workflows/reusable-node-framework-version-matrix.yml`

## Example

```yaml
jobs:
  svelte:
    uses: cobycloud/actions/.github/workflows/reusable-js-framework-ci.yml@main
    with:
      framework: svelte
      working-directory: apps/docs
      artifact-path: apps/docs/build
```

## Matrix Example

```yaml
jobs:
  frontend-matrix:
    uses: cobycloud/actions/.github/workflows/reusable-node-framework-version-matrix.yml@main
    with:
      node-versions: '["18","20","22"]'
      framework-cells: >-
        [
          {"framework":"svelte","working-directory":"apps/docs"},
          {"framework":"vue","working-directory":"apps/admin"},
          {"framework":"react","working-directory":"apps/client"}
        ]
```
