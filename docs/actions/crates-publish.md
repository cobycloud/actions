# crates.io Publish

Composite action: `cobycloud/actions/actions/crates-publish@main`

Publishes a Rust crate with `cargo publish`, including dry-run, workspace package selection, registry selection, feature controls, and canonical `CRATES_API_TOKEN` token handling.

## Use When

- A Rust crate should be published to crates.io.
- A workspace needs to publish one selected package.
- A release lane needs a reusable `cargo publish --dry-run` or real publish step.
- A workflow should fail clearly if a caller requests trusted publishing for crates.io. crates.io publishing is token-based in Cargo.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/crates-publish@main
    with:
      crates-api-token: ${{ secrets.CRATES_API_TOKEN }}
      package: my-crate
      dry-run: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `publish-mode` | `token` | `token` requires `crates-api-token`; `auto` uses a token when present and otherwise fails with a trusted-publishing unsupported message; `trusted` always fails because crates.io publishing is token-based. |
| `rust-toolchain` | `stable` | Rust toolchain. |
| `working-directory` | `.` | Directory containing `Cargo.toml`. |
| `crates-api-token` | empty | Optional `CRATES_API_TOKEN`. Required for crates.io publishing. |
| `registry` | empty | Optional Cargo registry name. Empty uses crates.io. |
| `package` | empty | Optional workspace package name. |
| `features` | empty | Optional feature list. |
| `all-features` | `false` | Adds `--all-features`. |
| `no-default-features` | `false` | Adds `--no-default-features`. |
| `dry-run` | `false` | Adds `--dry-run`. |
| `allow-dirty` | `false` | Adds `--allow-dirty`. |

## Dependencies

- `dtolnay/rust-toolchain@stable`
- Cargo registry token

## Related Reusable Workflow

Use `.github/workflows/reusable-crates-publish.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `CRATES_API_TOKEN` | no | Optional crates.io or custom Cargo registry token. Required for real publishing. |
