# Python Package Build

Composite action: `cobycloud/actions/actions/python-package-build@main`

Builds one Python package with `uv build` and optionally uploads the distribution directory.

## Use When

- A workflow needs to build a wheel and source distribution from one package root.
- A matrix job builds multiple packages by varying `project-path`, `out-dir`, and `artifact-name`.
- The package build artifact should be available to later jobs.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/python-package-build@main
    with:
      python-version: "3.12"
      project-path: pkgs/example-package
      out-dir: pkgs/example-package/dist
      artifact-name: example-package-dist
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `python-version` | `3.12` | Python version passed to `actions/setup-python`. |
| `project-path` | `.` | Package project path passed to `uv build --project`. |
| `out-dir` | `dist` | Distribution output directory. |
| `upload-artifact` | `true` | Uploads `out-dir` as a workflow artifact when true. |
| `artifact-name` | `python-dist` | Artifact name. |

## Dependencies

- `astral-sh/setup-uv@v7`
- `actions/setup-python@v5`
- `actions/upload-artifact@v4` when artifact upload is enabled
- Bash shell
- A checked-out repository

## Related Reusable Workflow

Use `.github/workflows/reusable-python-package-build.yml` when the caller wants checkout and artifact upload wrapped as a reusable job.
