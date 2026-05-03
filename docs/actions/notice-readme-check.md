# Notice README Check

Composite action: `cobycloud/actions/actions/notice-readme-check@main`

Verifies package root README, LICENSE/COPYING, NOTICE, and package-name consistency.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/notice-readme-check@main
    with:
      package-roots: |
        .
        packages/example
      require-notice: "false"
      package-name-required-in-readme: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `package-roots` | `.` | Newline-delimited package root directories. |
| `require-notice` | `false` | Require a NOTICE file in each root. |
| `require-license` | `true` | Require a LICENSE or COPYING file in each root. |
| `require-readme` | `true` | Require a README file in each root. |
| `package-name-required-in-readme` | `true` | Require manifest package name to appear in README. |
| `report-json` | `reports/notice-readme-check.json` | JSON report output path. |
| `report-md` | `reports/notice-readme-check.md` | Markdown report output path. |

## Outputs

| Output | Description |
| --- | --- |
| `report-json` | JSON report path. |
| `report-md` | Markdown report path. |

## Related Reusable Workflow

Use `.github/workflows/reusable-notice-readme-check.yml` for checkout and report artifact upload.
