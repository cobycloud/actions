# RPM Publish

`actions/rpm-publish` verifies RPM outputs and runs a caller-provided publication command for a YUM/DNF repository.

## Purpose

- Publish `.rpm` artifacts to RPM repository infrastructure.
- Support repository tooling such as `createrepo_c`, cloud uploads, or hosted package APIs.
- Fail before publish when no RPM package matches the expected path.

## Dependencies

- RPM package artifacts.
- Repository tooling installed by `setup-command` or already available on the runner.

## Reusable Workflows

- `.github/workflows/reusable-rpm-publish.yml`
- `.github/workflows/reusable-linux-package-publish.yml`

## Example

```yaml
jobs:
  rpm:
    uses: cobycloud/actions/.github/workflows/reusable-rpm-publish.yml@main
    with:
      package-path: dist/*.rpm
      publish-command: ./scripts/publish-rpm.sh dist/*.rpm
```
