# Netlify Deploy

`actions/netlify-deploy` deploys a static app directory to Netlify.

## Purpose

- Standardize Netlify CLI deployment.
- Support production and preview-style deploys.
- Keep Netlify site ID and auth token in caller secrets.

## Reusable Workflow

- `.github/workflows/reusable-netlify-deploy.yml`

## Example

```yaml
jobs:
  deploy:
    uses: cobycloud/actions/.github/workflows/reusable-netlify-deploy.yml@main
    with:
      build-command: npm run build
      output-path: dist
      production: true
    secrets:
      NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
      NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```
