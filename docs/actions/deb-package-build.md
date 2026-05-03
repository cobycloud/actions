# Debian Package Build

`actions/deb-package-build` builds Debian packages and uploads `.deb` outputs.

## Purpose

- Run Debian packaging commands such as `dpkg-buildpackage`.
- Support caller-owned setup for packaging dependencies.
- Upload generated `.deb` files for signing, attestation, release, or APT publication.

## Dependencies

- Debian packaging tools installed by the runner image or `setup-command`.
- `actions/upload-artifact`.

## Reusable Workflow

- `.github/workflows/reusable-deb-package-build.yml`

## Example

```yaml
jobs:
  deb:
    uses: cobycloud/actions/.github/workflows/reusable-deb-package-build.yml@main
    with:
      setup-command: sudo apt-get update && sudo apt-get install -y debhelper devscripts
      build-command: dpkg-buildpackage -us -uc -b
      artifact-path: ../*.deb
```
