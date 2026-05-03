# Static App Build

`actions/static-app-build` builds a static app and uploads the generated output.

## Purpose

- Build frontend/static assets once before deployment.
- Preserve deployable output as a workflow artifact.
- Support Vite, SvelteKit static output, Vue, React, Docusaurus, VitePress, and similar apps.

## Reusable Workflow

- `.github/workflows/reusable-static-app-build.yml`

## Example

```yaml
jobs:
  build:
    uses: cobycloud/actions/.github/workflows/reusable-static-app-build.yml@main
    with:
      build-command: npm run build
      output-path: dist
```
