# PyPI Token Publish

Composite action: `cobycloud/actions/actions/pypi-token-publish@main`

Publishes prebuilt Python distributions to PyPI or TestPyPI using a PyPI API token only. It does not attempt Trusted Publishing.

## Use When

- A prior job has already built wheels and source distributions.
- Publication must use a repository or project-scoped PyPI API token.
- The workflow should fail immediately if no token is provided.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/pypi-token-publish@main
    with:
      packages-dir: dist
      token: ${{ secrets.PYPI_API_TOKEN }}
      skip-existing: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `packages-dir` | `dist` | Directory containing distributions. |
| `repository-url` | empty | Optional repository URL, such as `https://test.pypi.org/legacy/`. |
| `token` | required | PyPI API token. |
| `skip-existing` | `false` | Do not fail if a distribution already exists. |

## Dependencies

- `uv publish`
