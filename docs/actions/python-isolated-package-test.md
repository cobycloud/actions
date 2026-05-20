# Python Isolated Package Test

Composite action: `cobycloud/actions/actions/python-isolated-package-test@main`

Tests one built Python wheel in an isolated virtual environment while optionally exposing sibling monorepo package sources.

## Use When

- A monorepo package matrix needs to prove each package installs from its own wheel.
- Tests should run against a clean environment instead of the caller workspace environment.
- Sibling workspace package sources should be available without publishing or building every sibling package.
- Package-specific tests live outside the package source tree and should run only when present.

## Behavior

1. Verifies the current Python minor version matches `python-version`.
2. Locates the built wheel in `wheel-dir`.
3. Creates a fresh virtual environment under `work-dir`.
4. Writes matching `workspace-source-globs` entries into a `.pth` file.
5. Installs the target wheel with `--no-deps`.
6. Optionally runs `pip check`.
7. Imports `import-root` and checks installed distribution metadata version.
8. Optionally runs `pre-test-command` with `VENV_PYTHON` and `VENV_BIN`
   available in the environment.
9. Runs package-specific pytest paths when those paths exist.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `python-version` | `3.12` | Python version expected in the current job. |
| `package-name` | required | Python distribution name under test. |
| `package-version` | required | Expected installed distribution version. |
| `import-root` | required | Import root to smoke import after wheel installation. |
| `wheel-dir` | required | Directory containing the built wheel. |
| `workspace-source-globs` | `pkgs/*/src` | Newline-separated source globs exposed through a `.pth` file. |
| `package-test-paths` | empty | Newline-separated pytest paths. Missing paths are ignored. |
| `work-dir` | `.tmp/python-isolated-package-test` | Temporary virtual environment root. |
| `install-pytest` | `true` | Install pytest before running package test paths. |
| `pip-check` | `true` | Run `pip check` after wheel install. |
| `pre-test-command` | empty | Optional command to run before package test paths. |

`pre-test-command` can use:

```text
VENV_PYTHON
VENV_BIN
PACKAGE_UNDER_TEST
IMPORT_ROOT_UNDER_TEST
PACKAGE_VERSION_UNDER_TEST
```

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"
  - uses: cobycloud/actions/actions/python-package-build@main
    with:
      python-version: "3.12"
      project-path: pkgs/example
      out-dir: dist/example-py312
      upload-artifact: "false"
  - uses: cobycloud/actions/actions/python-isolated-package-test@main
    with:
      python-version: "3.12"
      package-name: example
      package-version: "0.1.0"
      import-root: example
      wheel-dir: dist/example-py312
      workspace-source-globs: |
        pkgs/*/src
      package-test-paths: |
        tests/packages/example
        tests/packages/example_import_root
```

## Dependencies

- A checked-out repository
- `actions/setup-python` already run by the caller
- A built wheel in `wheel-dir`
- Bash shell
