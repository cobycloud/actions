# Artifact Attestation

Composite action: `cobycloud/actions/actions/artifact-attestation@main`

Generates build provenance attestations for build artifact paths using `actions/attest-build-provenance`.

## Example

```yaml
permissions:
  contents: read
  id-token: write
  attestations: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/artifact-attestation@main
    with:
      subject-path: dist/*
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `subject-path` | required | Path or glob of artifacts to attest. |
| `subject-name` | empty | Optional subject name. |
| `push-to-registry` | `false` | Push attestations to registry when supported. |
| `show-summary` | `true` | Show summary in the GitHub Actions summary. |

## Related Reusable Workflow

Use `.github/workflows/reusable-artifact-attestation.yml` for checkout and permissions.
