# Tauri Artifact Build

`actions/tauri-artifact-build` sets up Node and Rust, runs a Tauri build, and uploads generated bundles.

## Purpose

- Build Tauri desktop installers for Linux, Windows, or macOS.
- Install optional Linux system dependencies before the build.
- Upload generated Tauri bundles for release, signing, or attestation lanes.

## Dependencies

- `actions/setup-node`
- `dtolnay/rust-toolchain`
- `Swatinem/rust-cache`
- Tauri CLI and project dependencies installed by the caller's install command

## Reusable Workflow

- `.github/workflows/reusable-tauri-release.yml`

## Example

```yaml
jobs:
  tauri:
    uses: cobycloud/actions/.github/workflows/reusable-tauri-release.yml@main
    with:
      runner: ubuntu-latest
      linux-deps-command: sudo apt-get update && sudo apt-get install -y libwebkit2gtk-4.1-dev
```
