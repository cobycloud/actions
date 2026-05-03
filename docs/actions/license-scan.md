# License Scan

Composite action: `cobycloud/actions/actions/license-scan@main`

Scans Node, Python, and Rust package manifests for declared license metadata, finds license/notice files, emits JSON and Markdown reports, and optionally fails on missing or disallowed licenses.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/license-scan@main
    with:
      allowed-licenses: |
        MIT
        Apache-2.0
      fail-on-missing: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `manifest-globs` | common package manifests | Newline-delimited manifest glob patterns. |
| `license-file-globs` | common license/notice filenames | Newline-delimited license file glob patterns. |
| `allowed-licenses` | empty | Optional newline-delimited allowlist. Empty allows any declared license. |
| `fail-on-missing` | `true` | Fail when package manifests lack license metadata. |
| `fail-on-disallowed` | `true` | Fail when a license is outside `allowed-licenses`. |
| `report-json` | `reports/license-scan.json` | JSON report output path. |
| `report-md` | `reports/license-scan.md` | Markdown report output path. |

## Outputs

| Output | Description |
| --- | --- |
| `report-json` | JSON report path. |
| `report-md` | Markdown report path. |

## Related Reusable Workflow

Use `.github/workflows/reusable-license-scan.yml` for checkout and report artifact upload.
