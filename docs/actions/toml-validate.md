# TOML Validate

Composite action: `cobycloud/actions/actions/toml-validate@main`

Validates TOML syntax and required package metadata sections for `pyproject.toml`, `Cargo.toml`, and other TOML files.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/toml-validate@main
    with:
      toml-globs: |
        pyproject.toml
        pkgs/*/pyproject.toml
        Cargo.toml
        crates/*/Cargo.toml
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `toml-globs` | common Python/Rust TOML files | Newline-delimited TOML glob patterns. |
| `require-known-package-section` | `true` | Require `[project]`/`[tool.poetry]` or `[package]`/`[workspace]` in known manifests. |
| `report-json` | `reports/toml-validate.json` | JSON report output path. |
| `report-md` | `reports/toml-validate.md` | Markdown report output path. |

## Outputs

| Output | Description |
| --- | --- |
| `report-json` | JSON report path. |
| `report-md` | Markdown report path. |

## Related Reusable Workflow

Use `.github/workflows/reusable-toml-validate.yml` for checkout and report artifact upload.
