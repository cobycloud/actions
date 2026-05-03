# Rust Cargo CI

`actions/rust-cargo-ci` installs a Rust toolchain and runs the common Cargo CI sequence for one matrix cell.

## Purpose

- Install `stable`, `beta`, `nightly`, or an MSRV toolchain.
- Add `rustfmt`, `clippy`, and optional targets.
- Cache Cargo build and registry data.
- Run format, clippy, test, build, and optional documentation commands.

## Dependencies

- `dtolnay/rust-toolchain`
- `Swatinem/rust-cache`
- `cargo`, `rustfmt`, and `clippy`

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `rust-toolchain` | `stable` | Rust toolchain to install. |
| `working-directory` | `.` | Directory containing `Cargo.toml`. |
| `components` | `rustfmt,clippy` | Rust components to install. |
| `targets` | empty | Rust target triples to install. |
| `cache` | `true` | Enables Rust cache. |
| `fmt-command` | `cargo fmt --all -- --check` | Format gate. |
| `clippy-command` | `cargo clippy --all-targets --all-features -- -D warnings` | Lint gate. |
| `test-command` | `cargo test --all-features` | Test gate. |
| `build-command` | `cargo build --all-features` | Build gate. |
| `doc-command` | empty | Optional docs gate. |

## Reusable Workflows

- `.github/workflows/reusable-rust-ci.yml`
- `.github/workflows/reusable-rust-version-matrix.yml`
- `.github/workflows/reusable-cross-platform-rust.yml`
- `.github/workflows/reusable-os-matrix.yml`

## Example

```yaml
jobs:
  rust:
    uses: cobycloud/actions/.github/workflows/reusable-rust-version-matrix.yml@main
    with:
      rust-toolchains: '["1.75.0","stable","beta"]'
      test-command: cargo test --workspace --all-features
```
