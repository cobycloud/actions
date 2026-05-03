# crates.io Publish

Composite action: `cobycloud/actions/actions/crates-publish@main`

Publishes a Rust crate with `cargo publish`, including dry-run, workspace package selection, registry selection, and feature controls.

## Use When

- A Rust crate should be published to crates.io.
- A workspace needs to publish one selected package.
- A release lane needs a reusable `cargo publish --dry-run` or real publish step.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/crates-publish@main
    with:
      cargo-token: ${{ secrets.CARGO_REGISTRY_TOKEN }}
      package: my-crate
      dry-run: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `rust-toolchain` | `stable` | Rust toolchain. |
| `working-directory` | `.` | Directory containing `Cargo.toml`. |
| `cargo-token` | required | crates.io or registry token. |
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
| `CARGO_REGISTRY_TOKEN` | yes | crates.io or custom Cargo registry token. |
