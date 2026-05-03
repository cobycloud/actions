# PyPI Publish

Composite action: `cobycloud/actions/actions/pypi-publish@main`

Publishes prebuilt Python distributions to PyPI or TestPyPI using PyPI trusted publishing or an API token fallback.

## Use When

- A prior job has already built wheels and source distributions.
- The repository uses PyPI trusted publishing through `id-token: write`.
- The repository needs a reusable TestPyPI/PyPI publication step.

## Example

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/pypi-publish@main
    with:
      packages-dir: dist
```

## Token Example

```yaml
steps:
  - uses: cobycloud/actions/actions/pypi-publish@main
    with:
      packages-dir: dist
      password: ${{ secrets.PYPI_API_TOKEN }}
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `packages-dir` | `dist` | Directory or glob containing distributions. |
| `repository-url` | empty | Optional repository URL, such as `https://test.pypi.org/legacy/`. |
| `password` | empty | Optional PyPI API token. Empty uses trusted publishing. |
| `skip-existing` | `false` | Do not fail if a distribution already exists. |
| `verbose` | `false` | Enable verbose upload output. |
| `print-hash` | `true` | Print hashes for uploaded distributions. |

## Dependencies

- `pypa/gh-action-pypi-publish@release/v1`
- `id-token: write` for trusted publishing

## Related Reusable Workflow

Use `.github/workflows/reusable-pypi-publish.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `PYPI_TOKEN` | no | Optional PyPI API token. Omit for trusted publishing. |

Reusable workflow extra inputs:

| Input | Default | Description |
| --- | --- | --- |
| `artifact-name` | empty | Optional workflow artifact to download into `packages-dir` before publishing. |
