# Create Pull Request

`actions/create-pr` creates or updates a pull request for generated changes.

## Purpose

- Wrap `peter-evans/create-pull-request` with repository-standard inputs.
- Open PRs for generated docs, metadata, release prep, or monorepo output changes.
- Keep token and branch naming caller-owned.

## Reusable Workflow

- `.github/workflows/reusable-create-pr.yml`

## Example

```yaml
jobs:
  pr:
    uses: cobycloud/actions/.github/workflows/reusable-create-pr.yml@main
    with:
      paths: docs
      branch: update-docs
      title: Update generated docs
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
