# OS Matrix Cell

`actions/os-matrix-cell` runs one Node, Python, Rust, or generic validation cell on the current runner OS.

## Purpose

- Provide an action-level surface for reusable OS matrix jobs.
- Run Node, Python, or Rust defaults without requiring every caller to repeat setup steps.
- Support generic command dispatch through `actions/cross-platform-command`.

## Dependencies

- `actions/setup-node` for Node cells.
- `astral-sh/setup-uv` and `actions/setup-python` for Python cells.
- `dtolnay/rust-toolchain` and `Swatinem/rust-cache` for Rust cells.
- `actions/cross-platform-command` for generic cells.

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `ecosystem` | required | `node`, `python`, `rust`, or `generic`. |
| `version` | empty | Runtime/toolchain version. Empty uses ecosystem default. |
| `working-directory` | `.` | Directory where commands execute. |
| `install-command` | empty | Dependency install command. Empty uses ecosystem default where applicable. |
| `run-command` | empty | Main validation command. Empty uses ecosystem default where applicable. |
| `linux-command` | empty | Generic Linux override. |
| `macos-command` | empty | Generic macOS override. |
| `windows-command` | empty | Generic Windows override. |
| `compute-monorepo-pythonpath` | `false` | Adds repo root and package/src folders to `PYTHONPATH` for Python cells. |
| `rust-components` | `rustfmt,clippy` | Rust components to install. |
| `rust-targets` | empty | Rust targets to install. |

## Reusable Workflows

- `.github/workflows/reusable-os-matrix.yml`
- `.github/workflows/reusable-cross-platform-node.yml`
- `.github/workflows/reusable-cross-platform-python.yml`
- `.github/workflows/reusable-cross-platform-rust.yml`

## Example

```yaml
jobs:
  os:
    uses: cobycloud/actions/.github/workflows/reusable-os-matrix.yml@main
    with:
      ecosystem: python
      version: "3.12"
      run-command: uv run pytest
```
