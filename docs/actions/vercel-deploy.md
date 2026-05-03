# Vercel Deploy

`actions/vercel-deploy` deploys a static app or frontend project to Vercel.

## Purpose

- Standardize Vercel CLI deployment.
- Support production or preview deployment modes.
- Keep Vercel token and optional org/project IDs in caller secrets.

## Reusable Workflow

- `.github/workflows/reusable-vercel-deploy.yml`

## Example

```yaml
jobs:
  deploy:
    uses: cobycloud/actions/.github/workflows/reusable-vercel-deploy.yml@main
    with:
      build-command: npm run build
      production: true
    secrets:
      VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
      VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
      VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```
