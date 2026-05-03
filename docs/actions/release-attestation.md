# Release Attestation

Composite action: `cobycloud/actions/actions/release-attestation@main`

Generates build provenance attestations for release asset files.

## Example

```yaml
permissions:
  contents: read
  id-token: write
  attestations: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/release-attestation@main
    with:
      release-assets-path: release-assets/*
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `release-assets-path` | `release-assets/*` | Path or glob containing release assets. |
| `subject-name` | empty | Optional subject name. |
| `push-to-registry` | `false` | Push attestations to registry when supported. |
| `show-summary` | `true` | Show summary in the GitHub Actions summary. |

## Related Reusable Workflow

Use `.github/workflows/reusable-release-attestation.yml` for checkout and permissions.
