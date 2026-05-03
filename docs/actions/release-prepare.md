# Release Prepare

Composite action: `cobycloud/actions/actions/release-prepare@main`

Computes release version metadata, tag name, release name, and release notes from a changelog.

## Use When

- A release pipeline needs normalized tag and release-name outputs.
- Release notes should be extracted from `CHANGELOG.md`.
- A workflow should validate that version-bearing files contain the target version.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - id: prepare
    uses: cobycloud/actions/actions/release-prepare@main
    with:
      version: "1.2.3"
      tag-prefix: v
      changelog-path: CHANGELOG.md
      validate-version-files: |
        pyproject.toml
        package.json
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `version` | required | Release version without tag prefix. |
| `tag-prefix` | `v` | Prefix used when computing the release tag. |
| `release-name` | empty | Explicit release display name. Defaults to computed tag. |
| `changelog-path` | `CHANGELOG.md` | Changelog used to extract release notes. |
| `release-notes-output` | `release-notes.md` | File where release notes are written. |
| `fallback-notes` | empty | Notes used when no changelog section matches. |
| `validate-clean` | `false` | Fail if the git working tree is dirty. |
| `validate-version-files` | empty | Newline-delimited files that must contain the target version. |

## Outputs

| Output | Description |
| --- | --- |
| `version` | Release version. |
| `tag-name` | Computed tag name. |
| `release-name` | Computed release display name. |
| `release-notes` | Release notes output path. |

## Related Reusable Workflow

Use `.github/workflows/reusable-release-prepare.yml` for the full reusable job wrapper.
