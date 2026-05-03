# Version Bump

Composite action: `cobycloud/actions/actions/version-bump@main`

Bumps versions in `package.json`, `pyproject.toml`, `Cargo.toml`, and caller-specified release metadata files.

## Use When

- A release workflow needs a reusable version mutation step.
- A repository has Python, Node, Rust, or mixed package manifests.
- A version bump should be separated from publication.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/version-bump@main
    with:
      version: "1.2.3"
      package-json-files: |
        package.json
        packages/*/package.json
      pyproject-files: |
        pyproject.toml
        pkgs/*/pyproject.toml
      cargo-files: |
        Cargo.toml
        crates/*/Cargo.toml
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `version` | required | Version to write, without tag prefix. |
| `package-json-files` | `package.json` | Newline-delimited `package.json` glob patterns. |
| `pyproject-files` | `pyproject.toml` | Newline-delimited `pyproject.toml` glob patterns. |
| `cargo-files` | `Cargo.toml` | Newline-delimited `Cargo.toml` glob patterns. |
| `extra-version-files` | empty | Newline-delimited extra files for regex-based version replacement. |
| `extra-version-pattern` | version assignment regex | Regex with two capture groups around the version text for extra files. |
| `update-lockfiles` | `false` | Refresh npm and Cargo lockfiles when true. |
| `npm-lock-command` | `npm install --package-lock-only --ignore-scripts` | npm lockfile refresh command. |
| `cargo-lock-command` | `cargo generate-lockfile` | Cargo lockfile refresh command. |

## Outputs

| Output | Description |
| --- | --- |
| `changed` | Whether any file content changed. |
| `changed-files` | Newline-delimited changed file paths. |

## Related Reusable Workflow

Use `.github/workflows/reusable-version-bump.yml` for the full reusable job wrapper.
