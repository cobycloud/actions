# Sign Artifacts

Composite action: `cobycloud/actions/actions/sign-artifacts@main`

Signs files with cosign. Empty key input uses keyless signing through GitHub OIDC; provided key input uses key-based signing.

## Example

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/sign-artifacts@main
    with:
      artifact-path: release-assets
```

## Key-Based Example

```yaml
steps:
  - uses: cobycloud/actions/actions/sign-artifacts@main
    with:
      artifact-path: release-assets/*
      key: ${{ secrets.COSIGN_PRIVATE_KEY }}
      password: ${{ secrets.COSIGN_PASSWORD }}
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `artifact-path` | required | Path or glob of files to sign. |
| `cosign-version` | `latest` | Cosign version to install. |
| `key` | empty | Optional cosign private key. Empty uses keyless signing. |
| `password` | empty | Optional cosign private key password. |
| `recursive` | `true` | Expand files recursively when `artifact-path` is a directory. |
| `output-signatures` | `true` | Reserved marker for workflows that upload generated signature files. |

## Related Reusable Workflow

Use `.github/workflows/reusable-sign-artifacts.yml` for checkout, permissions, optional signing secrets, and signature artifact upload.
