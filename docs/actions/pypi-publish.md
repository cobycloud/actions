# PyPI Publish

Composite action: `cobycloud/actions/actions/pypi-publish@main`

Publishes prebuilt Python distributions to PyPI or TestPyPI using PyPI trusted publishing or an API token fallback.

This is the compatibility action. Prefer the explicit actions for new workflows:

- `cobycloud/actions/actions/pypi-token-publish@main` for API-token-only publishing.
- `cobycloud/actions/actions/pypi-trusted-publish@main` for Trusted-Publishing-only publishing.

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
      publish-mode: auto
      api-token: ${{ secrets.PYPI_API_TOKEN }}
```

## Token Example

```yaml
steps:
  - uses: cobycloud/actions/actions/pypi-token-publish@main
    with:
      packages-dir: dist
      api-token: ${{ secrets.PYPI_API_TOKEN }}
```

## Trusted Publishing Example

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: cobycloud/actions/actions/pypi-trusted-publish@main
    with:
      packages-dir: dist
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `publish-mode` | `auto` | `token` requires `api-token`; `trusted` requires PyPI Trusted Publishing; `auto` uses `api-token` when present and otherwise uses trusted publishing. |
| `packages-dir` | `dist` | Directory or glob containing distributions. |
| `repository-url` | empty | Optional repository URL, such as `https://test.pypi.org/legacy/`. |
| `api-token` | empty | Optional `PYPI_API_TOKEN`. Required when `publish-mode` is `token`. |
| `skip-existing` | `false` | Do not fail if a distribution already exists. |
| `verbose` | `false` | Enable verbose upload output. |
| `print-hash` | `true` | Print hashes for uploaded distributions. |

## Dependencies

- `uv publish`
- `id-token: write` for trusted publishing

## Explicit Action Docs

- [`pypi-token-publish.md`](pypi-token-publish.md)
- [`pypi-trusted-publish.md`](pypi-trusted-publish.md)

## Related Reusable Workflow

Use `.github/workflows/reusable-pypi-publish.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `PYPI_API_TOKEN` | no | Optional PyPI API token. Required only when `publish-mode` is `token`. |

Reusable workflow extra inputs:

| Input | Default | Description |
| --- | --- | --- |
| `artifact-name` | empty | Optional workflow artifact to download into `packages-dir` before publishing. |
| `publish-mode` | `auto` | `token`, `trusted`, or `auto`. |
