# Python Package CI

`actions/python-package-ci` runs install, compile, test, docs, build, and optional artifact upload checks for one Python package matrix cell.

## Purpose

- Validate a package directory across Python versions.
- Run compile/import smoke checks with `compileall`.
- Run package tests and optional docs/build commands.
- Support monorepo `PYTHONPATH` computation for package trees.

## Dependencies

- `astral-sh/setup-uv`
- `actions/setup-python`
- `actions/upload-artifact`
- `uv`
- Optional test/doc/build tools installed by the caller's install command

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `python-version` | `3.12` | Python version to install. |
| `package-path` | `.` | Package directory to validate. |
| `install-command` | `uv sync --all-groups --frozen` | Dependency install command. |
| `compile-command` | `uv run python -m compileall .` | Compile/import smoke gate. |
| `test-command` | `uv run pytest` | Test gate. |
| `docs-command` | empty | Optional docs gate. |
| `build-command` | empty | Optional package build gate. |
| `compute-monorepo-pythonpath` | `false` | Adds repo root and `pkgs/*/*` package/src folders to `PYTHONPATH`. |
| `artifact-path` | empty | Optional path to upload after checks. |

## Reusable Workflow

- `.github/workflows/reusable-python-package-matrix-ci.yml`

## Example

```yaml
jobs:
  package-matrix:
    uses: cobycloud/actions/.github/workflows/reusable-python-package-matrix-ci.yml@main
    with:
      python-versions: '["3.10","3.11","3.12","3.13"]'
      package-cells: >-
        [
          {"name":"core","path":"pkgs/core/example"},
          {"name":"plugin","path":"pkgs/plugins/example"}
        ]
      compute-monorepo-pythonpath: true
```
