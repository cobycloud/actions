# Verify Attestations

Composite action: `cobycloud/actions/actions/verify-attestations@main`

Verifies GitHub artifact attestations with `gh attestation verify` and optionally verifies adjacent cosign signatures.

## Example

```yaml
permissions:
  contents: read
  attestations: read

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/verify-attestations@main
    with:
      subject-path: release-assets/*
      verify-gh-attestations: "true"
```

## Cosign Example

```yaml
steps:
  - uses: cobycloud/actions/actions/verify-attestations@main
    with:
      subject-path: release-assets/*
      verify-cosign-signatures: "true"
      certificate-identity: https://github.com/example/repo/.github/workflows/release.yml@refs/tags/v1.2.3
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `subject-path` | required | Path or glob of artifacts to verify. |
| `owner` | current repository owner | Expected GitHub owner. |
| `repo` | current repository | Expected repository in `owner/name` form. |
| `verify-gh-attestations` | `true` | Verify GitHub artifact attestations. |
| `verify-cosign-signatures` | `false` | Verify adjacent `.sig` files. |
| `cosign-version` | `latest` | Cosign version to install. |
| `certificate-identity` | empty | Expected keyless certificate identity. |
| `certificate-oidc-issuer` | `https://token.actions.githubusercontent.com` | Expected OIDC issuer. |
| `key` | empty | Optional public key for key-based cosign verification. |

## Related Reusable Workflow

Use `.github/workflows/reusable-verify-attestations.yml` for checkout, permissions, and optional public-key secret wiring.
