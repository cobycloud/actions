# Cloudflare Pages Deploy

`actions/cloudflare-pages-deploy` deploys a static app directory to Cloudflare Pages with Wrangler.

## Purpose

- Standardize Cloudflare Pages deployment.
- Keep Cloudflare credentials in caller secrets.
- Support optional setup/build before deployment.

## Reusable Workflow

- `.github/workflows/reusable-cloudflare-pages-deploy.yml`

## Example

```yaml
jobs:
  deploy:
    uses: cobycloud/actions/.github/workflows/reusable-cloudflare-pages-deploy.yml@main
    with:
      project-name: docs
      build-command: npm run build
      output-path: dist
    secrets:
      CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```
