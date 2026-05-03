# Docs Build

`actions/docs-build` builds documentation with caller-provided commands and uploads the generated site.

## Purpose

- Build MkDocs, Sphinx, VitePress, Docusaurus, or custom docs sites.
- Keep docs tooling caller-owned.
- Upload the generated site for Pages deployment, release attachment, or inspection.

## Dependencies

- Docs tooling installed by `setup-command` or the checked-out project.
- `actions/upload-artifact`.

## Reusable Workflows

- `.github/workflows/reusable-docs-build.yml`
- `.github/workflows/reusable-docs-release.yml`

## Example

```yaml
jobs:
  docs:
    uses: cobycloud/actions/.github/workflows/reusable-docs-build.yml@main
    with:
      setup-command: uv sync --all-groups --frozen
      build-command: uv run mkdocs build
      output-path: site
```
