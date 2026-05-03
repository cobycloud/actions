# Git Commit Generated

`actions/git-commit-generated` commits generated outputs and can optionally push them to the current branch.

## Purpose

- Commit generated files without assuming a frontend `dist` directory.
- Support docs, registries, manifests, release metadata, or other generated outputs.
- Return whether a commit was created.

## Reusable Workflow

- `.github/workflows/reusable-git-commit-generated.yml`

## Example

```yaml
jobs:
  commit:
    uses: cobycloud/actions/.github/workflows/reusable-git-commit-generated.yml@main
    with:
      paths: |
        docs
        .ssot/registry.json
      commit-message: Update generated docs
```
