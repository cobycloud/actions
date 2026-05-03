# Linux Package Publish

`reusable-linux-package-publish.yml` routes Linux package publication to APT, RPM, Snapcraft, or Homebrew tap update lanes.

## Purpose

- Provide one reusable workflow for package-manager-specific publication.
- Route `apt`, `rpm`, `snap`, and `brew` publication through the dedicated actions.
- Keep provider-specific credentials and repository tooling caller-owned.

## Dependencies

- `actions/apt-publish` for APT repositories.
- `actions/rpm-publish` for YUM/DNF repositories.
- `actions/snap-publish` for Snapcraft.
- `actions/brew-publish` for Homebrew taps.

## Reusable Workflow

- `.github/workflows/reusable-linux-package-publish.yml`

## Example

```yaml
jobs:
  publish:
    uses: cobycloud/actions/.github/workflows/reusable-linux-package-publish.yml@main
    with:
      package-manager: apt
      package-path: dist/*.deb
      publish-command: ./scripts/publish-apt.sh dist/*.deb
```
