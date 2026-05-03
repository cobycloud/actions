# Package Metadata

Composite action: `cobycloud/actions/actions/package-metadata@main`

Validates manifest parseability and baseline metadata for `package.json`, `pyproject.toml`, and `Cargo.toml`.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/package-metadata@main
    with:
      require-description: "true"
      require-license: "true"
      require-readme: "true"
      require-url: "false"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `manifest-globs` | common package manifests | Newline-delimited manifest glob patterns. |
| `require-description` | `true` | Require non-empty descriptions. |
| `require-license` | `true` | Require license metadata. |
| `require-readme` | `true` | Require readme metadata or nearby README file. |
| `require-url` | `false` | Require homepage/repository/project URLs. |
| `report-json` | `reports/package-metadata.json` | JSON report output path. |
| `report-md` | `reports/package-metadata.md` | Markdown report output path. |

## Outputs

| Output | Description |
| --- | --- |
| `report-json` | JSON report path. |
| `report-md` | Markdown report path. |

## Related Reusable Workflow

Use `.github/workflows/reusable-package-metadata.yml` for checkout and report artifact upload.
