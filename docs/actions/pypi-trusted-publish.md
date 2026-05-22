# PyPI Trusted Publish

Composite action: `cobycloud/actions/actions/pypi-trusted-publish@main`

Publishes prebuilt Python distributions to PyPI or TestPyPI using PyPI Trusted Publishing only. It does not accept or use a PyPI API token.

## Use When

- A prior job has already built wheels and source distributions.
- The PyPI project has a trusted publisher configured for the calling workflow.
- The GitHub job grants `id-token: write`.

## Example

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/pypi-trusted-publish@main
    with:
      packages-dir: dist
      skip-existing: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `packages-dir` | `dist` | Directory containing distributions. |
| `repository-url` | empty | Optional repository URL, such as `https://test.pypi.org/legacy/`. |
| `skip-existing` | `false` | Do not fail if a distribution already exists. |

## Dependencies

- `uv publish`
- `id-token: write`
