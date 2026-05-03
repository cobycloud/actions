# Snap Publish

`actions/snap-publish` publishes a Snap package to Snapcraft.

## Purpose

- Publish `.snap` outputs to one or more Snapcraft channels.
- Keep Snapcraft credentials in GitHub Actions secrets.
- Provide a reusable wrapper around Snapcraft publication.

## Dependencies

- `snapcore/action-publish`
- `SNAPCRAFT_STORE_CREDENTIALS` secret
- A built `.snap` artifact available in the workspace

## Reusable Workflow

- `.github/workflows/reusable-snap-publish.yml`

## Example

```yaml
jobs:
  snap:
    uses: cobycloud/actions/.github/workflows/reusable-snap-publish.yml@main
    with:
      snap-file: dist/myapp.snap
      release: stable
    secrets:
      SNAPCRAFT_STORE_CREDENTIALS: ${{ secrets.SNAPCRAFT_STORE_CREDENTIALS }}
```
