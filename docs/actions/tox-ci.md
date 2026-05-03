# tox CI

`actions/tox-ci` sets up Python, installs tox, and runs tox environments for one matrix cell.

## Purpose

- Support repositories that already encode Python fan-out in `tox.ini`, `pyproject.toml`, or `setup.cfg`.
- Keep tox installation configurable for `tox-uv`, `tox-gh-actions`, and other plugins.
- Run a caller-provided tox command from a package subdirectory.

## Dependencies

- `actions/setup-python`
- `tox`
- Optional tox plugins installed by `install-command`

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `python-version` | `3.12` | Python interpreter used to run tox. |
| `working-directory` | `.` | Directory containing tox config. |
| `install-command` | `python -m pip install tox` | tox installation command. |
| `tox-command` | `tox` | tox execution command. |
| `cache` | `pip` | Cache mode for `actions/setup-python`. |

## Reusable Workflow

- `.github/workflows/reusable-tox.yml`
- `.github/workflows/reusable-tox-matrix.yml`

For Python version fan-out with `uv`, use `.github/workflows/reusable-python-version-matrix.yml` or `.github/workflows/reusable-cross-platform-python.yml`.

## Example

```yaml
jobs:
  tox:
    uses: cobycloud/actions/.github/workflows/reusable-tox.yml@main
    with:
      install-command: python -m pip install tox tox-uv
      tox-command: tox -p auto
```
