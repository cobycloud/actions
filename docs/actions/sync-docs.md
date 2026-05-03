# Sync Docs

`actions/sync-docs` runs a docs sync command and opens a pull request for changed docs.

## Purpose

- Sync versioned docs, generated API docs, or static documentation exports.
- Keep the sync command caller-owned.
- Open a PR with only the configured docs paths.

## Reusable Workflow

- `.github/workflows/reusable-sync-docs.yml`

## Example

```yaml
jobs:
  sync-docs:
    uses: cobycloud/actions/.github/workflows/reusable-sync-docs.yml@main
    with:
      sync-command: npm run docs:sync
      paths: docs
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
