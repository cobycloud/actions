# Electron Artifact Build

`actions/electron-artifact-build` installs Node dependencies, runs an Electron packaging command, and uploads desktop installers.

## Purpose

- Build Electron desktop artifacts from npm projects.
- Support Electron Builder, Forge, or custom package commands.
- Upload generated installers for GitHub Release, signing, or attestation lanes.

## Dependencies

- `actions/setup-node`
- npm or another package manager through caller-provided commands
- Electron packaging tooling installed by the project

## Reusable Workflow

- `.github/workflows/reusable-electron-release.yml`

## Example

```yaml
jobs:
  electron:
    uses: cobycloud/actions/.github/workflows/reusable-electron-release.yml@main
    with:
      runner: windows-latest
      build-command: npm run dist -- --win
      artifact-path: dist/*.exe
```
