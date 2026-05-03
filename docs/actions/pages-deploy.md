# Pages Deploy

`actions/pages-deploy` uploads a static site path and deploys it to GitHub Pages.

## Purpose

- Normalize GitHub Pages deployment boilerplate.
- Use GitHub's native Pages artifact and deployment actions.
- Keep docs build separate from deployment when desired.

## Dependencies

- `actions/configure-pages`
- `actions/upload-pages-artifact`
- `actions/deploy-pages`
- `pages: write` and `id-token: write` permissions

## Reusable Workflows

- `.github/workflows/reusable-pages-deploy.yml`
- `.github/workflows/reusable-docs-release.yml`

## Example

```yaml
jobs:
  pages:
    uses: cobycloud/actions/.github/workflows/reusable-pages-deploy.yml@main
    with:
      path: site
```
