# Snap Build

`actions/snap-build` builds Snap packages and uploads `.snap` outputs.

## Purpose

- Run Snapcraft builds from a repository-local `snapcraft.yaml`.
- Allow caller-owned setup for Snapcraft installation or build prerequisites.
- Upload built `.snap` files for signing, attestation, release, or Snapcraft publication.

## Dependencies

- Snapcraft installed by the runner image or `setup-command`.
- `actions/upload-artifact`.

## Reusable Workflow

- `.github/workflows/reusable-snap-build.yml`

## Example

```yaml
jobs:
  snap:
    uses: cobycloud/actions/.github/workflows/reusable-snap-build.yml@main
    with:
      setup-command: sudo snap install snapcraft --classic
      build-command: snapcraft --destructive-mode
```
