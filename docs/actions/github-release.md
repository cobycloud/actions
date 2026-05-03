# GitHub Release

Composite action: `cobycloud/actions/actions/github-release@main`

Creates or updates a GitHub Release and uploads matching files.

## Use When

- A release job needs to publish artifacts to a GitHub Release.
- Assets were prepared by a previous job or by `release-assets`.
- The caller needs consistent draft, prerelease, latest, and unmatched-file behavior.

## Example

```yaml
permissions:
  contents: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/github-release@main
    with:
      tag-name: v1.2.3
      name: v1.2.3
      files: |
        release-assets/*
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `tag-name` | required | Release tag name. |
| `name` | empty | Release display name. Defaults to tag when empty. |
| `body` | empty | Inline release body. |
| `body-path` | empty | Path to release notes file. |
| `files` | empty | Newline-delimited file globs. |
| `draft` | `false` | Create or keep release as draft. |
| `prerelease` | `false` | Mark release as prerelease. |
| `make-latest` | `legacy` | Latest release handling. |
| `fail-on-unmatched-files` | `true` | Fail if file globs do not match. |
| `token` | empty | Optional explicit GitHub token. Empty uses the action default. |

## Dependencies

- `softprops/action-gh-release@v2`
- Caller workflow permission `contents: write`

## Related Reusable Workflow

Use `.github/workflows/reusable-github-release.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `GH_TOKEN` | no | Optional explicit GitHub token. Omit to use `github.token`. |
