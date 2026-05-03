# Dependency Review

Composite action: `cobycloud/actions/actions/dependency-review@main`

Runs GitHub dependency review with reusable vulnerability, package, and license policy inputs.

## Example

```yaml
permissions:
  contents: read
  pull-requests: read

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/dependency-review@main
    with:
      fail-on-severity: high
      deny-licenses: GPL-3.0,AGPL-3.0
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `fail-on-severity` | `high` | Minimum vulnerability severity that fails the job. |
| `allow-licenses` | empty | Comma-separated allowed licenses. |
| `deny-licenses` | empty | Comma-separated denied licenses. |
| `deny-packages` | empty | Comma-separated denied package specifiers. |
| `allow-dependencies-licenses` | empty | Comma-separated packages exempted from license policy. |
| `vulnerability-check` | `true` | Enable vulnerability checks. |
| `license-check` | `true` | Enable license checks. |
| `comment-summary-in-pr` | `never` | Whether to comment a summary in PRs. |
| `retry-on-snapshot-warnings` | `true` | Retry when dependency snapshot warnings occur. |
| `config-file` | empty | Optional dependency review config file. |
| `checkout` | `false` | Checkout repository before dependency review. |

## Permissions

The caller should grant:

```yaml
permissions:
  contents: read
  pull-requests: read
```

## Related Reusable Workflow

Use `.github/workflows/reusable-dependency-review.yml` for checkout, permissions, and the full dependency review job wrapper.
