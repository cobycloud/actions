# Build and Commit Dist

Composite action: `cobycloud/actions/actions/build-and-commit-dist@main`

Builds a Node project and commits generated distribution output when the target output path changes.

## Use When

- A repository commits generated frontend output such as `client/dist`.
- The workflow needs a repeatable bot commit pattern after build.
- The caller can grant `contents: write`.

## Example

```yaml
permissions:
  contents: write

steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0
  - uses: cobycloud/actions/actions/build-and-commit-dist@main
    with:
      working-directory: client
      install-command: npm ci
      build-command: npm run build
      dist-path: client/dist
      commit-message: "chore(dist): update build output"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `node-version` | `20` | Node.js version passed to `actions/setup-node`. |
| `working-directory` | `client` | Directory containing `package.json`. |
| `install-command` | `npm ci` | Dependency install command. |
| `build-command` | `npm run build` | Build command. |
| `dist-path` | `client/dist` | Generated output path, relative to repo root. |
| `commit-message` | `chore(dist): update build output` | Commit message for generated output. |
| `bot-name` | `github-actions[bot]` | Git author name. |
| `bot-email` | `github-actions[bot]@users.noreply.github.com` | Git author email. |

## Outputs

| Output | Description |
| --- | --- |
| `committed` | `true` when a dist commit was created, otherwise `false`. |

## Dependencies

- `actions/setup-node@v4`
- Bash shell
- Git push permission through `GITHUB_TOKEN`
- Caller workflow permission `contents: write`

## Related Reusable Workflow

Use `.github/workflows/reusable-build-and-commit-dist.yml` when the caller wants checkout, concurrency, permissions, and the commit job wrapper.
