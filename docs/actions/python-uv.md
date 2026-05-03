# Python uv

Composite action: `cobycloud/actions/actions/python-uv@main`

Sets up `uv` and Python, installs dependencies, optionally computes a monorepo `PYTHONPATH`, and runs one validation command.

## Use When

- A Python repository or package uses `uv`.
- The caller wants a configurable install command and a configurable validation command.
- A monorepo needs package and `src` directories added to `PYTHONPATH`.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/python-uv@main
    with:
      python-version: "3.12"
      working-directory: backend
      install-command: uv pip install -e . pytest
      run-command: uv run pytest
```

## Monorepo Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/python-uv@main
    with:
      compute-monorepo-pythonpath: "true"
      install-command: uv sync --all-groups --no-install-workspace --frozen
      run-command: uv run --no-sync python tools/ci/validate_gate.py
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `python-version` | `3.12` | Python version passed to `actions/setup-python`. |
| `working-directory` | `.` | Directory where install and run commands execute. |
| `install-command` | `uv sync --all-groups --frozen` | Dependency installation command. |
| `run-command` | `uv run pytest` | Main validation command. Empty skips the command step. |
| `compute-monorepo-pythonpath` | `false` | Adds repo root and `pkgs/*/*` package/src folders to `PYTHONPATH`. |
| `uv-cache` | `true` | Enables `astral-sh/setup-uv` cache. |

## Dependencies

- `astral-sh/setup-uv@v7`
- `actions/setup-python@v5`
- Bash shell
- A checked-out repository

## Related Reusable Workflows

- `.github/workflows/reusable-python-uv-ci.yml`: one Python/uv CI job.
- `.github/workflows/reusable-python-version-matrix.yml`: Python 3.10 through 3.13 fan-out by default.
- `.github/workflows/reusable-cross-platform-python.yml`: Python version fan-out across Ubuntu, Windows, and macOS.
- `.github/workflows/reusable-python-package-matrix-ci.yml`: package-cell fan-out across Python versions.
- `.github/workflows/reusable-os-matrix.yml`: generic Node, Python, or Rust OS fan-out.
