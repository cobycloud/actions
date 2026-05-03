# APT Publish

`actions/apt-publish` verifies Debian package outputs and runs a caller-provided publication command for an APT repository.

## Purpose

- Publish `.deb` artifacts to an APT repository.
- Keep repository-specific tooling such as aptly, reprepro, or cloud upload commands caller-owned.
- Fail before publish when no Debian packages match the expected path.

## Dependencies

- Debian package artifacts.
- APT repository tooling installed by `setup-command` or already available on the runner.

## Reusable Workflow

- `.github/workflows/reusable-apt-publish.yml`

## Example

```yaml
jobs:
  apt:
    uses: cobycloud/actions/.github/workflows/reusable-apt-publish.yml@main
    with:
      package-path: dist/*.deb
      publish-command: ./scripts/publish-apt.sh dist/*.deb
```
