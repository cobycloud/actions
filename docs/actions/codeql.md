# CodeQL

Composite action: `cobycloud/actions/actions/codeql@main`

Runs CodeQL init, optional autobuild, and analyze for one or more languages.

## Example

```yaml
permissions:
  contents: read
  security-events: write
  actions: read

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/codeql@main
    with:
      languages: javascript-typescript
      build-mode: autobuild
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `languages` | required | Comma-separated CodeQL languages. |
| `build-mode` | `autobuild` | CodeQL build mode, such as `none`, `autobuild`, or `manual`. |
| `queries` | empty | Optional CodeQL query suites or packs. |
| `config-file` | empty | Optional CodeQL config file path. |
| `category` | empty | Optional analysis category. |
| `upload` | `true` | Upload CodeQL results. |
| `checkout` | `false` | Checkout repository before CodeQL. |

## Permissions

The caller should grant:

```yaml
permissions:
  contents: read
  security-events: write
  actions: read
```

## Related Reusable Workflow

Use `.github/workflows/reusable-codeql.yml` for checkout, permissions, and the full CodeQL job wrapper.
