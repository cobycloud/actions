# Static App Deploy

`actions/static-app-deploy` runs optional setup/build commands and a caller-owned provider deployment command.

## Purpose

- Deploy static apps to provider-specific hosting without baking provider details into the shared action.
- Support Cloudflare Pages, Netlify, Vercel, S3, Azure Static Web Apps, or custom hosting commands.
- Optionally upload deployment artifacts for diagnostics.

## Dependencies

- Provider CLI installed by `setup-command` or project dependencies.
- Deployment credentials supplied by the caller workflow.

## Reusable Workflow

- `.github/workflows/reusable-static-app-deploy.yml`

## Example

```yaml
jobs:
  deploy:
    uses: cobycloud/actions/.github/workflows/reusable-static-app-deploy.yml@main
    with:
      build-command: npm run build
      deploy-command: npx wrangler pages deploy dist --project-name docs
```
