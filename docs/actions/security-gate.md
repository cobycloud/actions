# Security Gate

Composite action: `cobycloud/actions/actions/security-gate@main`

Aggregates baseline security and compliance checks: license scan, package metadata, TOML validation, dependency review, and optional CodeQL.

## Example

```yaml
permissions:
  contents: read
  pull-requests: read
  security-events: write
  actions: read

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/security-gate@main
    with:
      run-dependency-review: "true"
      run-codeql: "true"
      codeql-languages: javascript-typescript
      allowed-licenses: |
        MIT
        Apache-2.0
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `run-license-scan` | `true` | Run license scan. |
| `run-package-metadata` | `true` | Run package metadata validation. |
| `run-toml-validate` | `true` | Run TOML validation. |
| `run-dependency-review` | `false` | Run dependency review. Usually only valid for pull request events. |
| `run-codeql` | `false` | Run CodeQL analysis. |
| `codeql-languages` | empty | Comma-separated CodeQL languages when `run-codeql` is true. |
| `codeql-build-mode` | `autobuild` | CodeQL build mode. |
| `dependency-fail-on-severity` | `high` | Dependency review severity threshold. |
| `allowed-licenses` | empty | Newline-delimited license scan allowlist. |
| `dependency-allow-licenses` | empty | Comma-separated dependency-review allowed licenses. |
| `dependency-deny-licenses` | empty | Comma-separated dependency-review denied licenses. |

## Permissions

Enable permissions based on selected checks:

```yaml
permissions:
  contents: read
  pull-requests: read
  security-events: write
  actions: read
```

## Related Reusable Workflow

Use `.github/workflows/reusable-security-gate.yml` for checkout, permissions, report upload, and the full aggregate job wrapper.
