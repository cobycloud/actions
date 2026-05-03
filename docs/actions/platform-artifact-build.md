# Platform Artifact Build

`actions/platform-artifact-build` runs a setup command, runs a platform build command, and uploads the produced artifact.

## Purpose

- Build Linux, Windows, or Darwin artifacts with a caller-owned command.
- Keep platform-specific packaging commands outside repeated workflow boilerplate.
- Use Linux, macOS, or Windows build command overrides when shell syntax differs.
- Upload installers, archives, binaries, or bundle directories.

## Dependencies

- `actions/upload-artifact`
- Build tools installed by the runner image or `setup-command`

## Reusable Workflows

- `.github/workflows/reusable-build-linux-artifact.yml`
- `.github/workflows/reusable-build-windows-artifact.yml`
- `.github/workflows/reusable-build-darwin-artifact.yml`

## Example

```yaml
jobs:
  linux:
    uses: cobycloud/actions/.github/workflows/reusable-build-linux-artifact.yml@main
    with:
      build-command: cargo build --release
      artifact-path: target/release/myapp
```
