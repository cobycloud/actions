# Setup Node Project

Composite action: `cobycloud/actions/actions/setup-node-project@main`

Installs Node, installs package dependencies, and optionally runs build and test commands from a configurable package directory.

## Use When

- A workflow already checks out the repository and needs a repeatable Node install/build/test step block.
- The project uses `npm ci`, `npm install`, or another caller-supplied install command.
- Build and test commands vary by repository but the setup pattern is the same.

## Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/setup-node-project@main
    with:
      node-version: "20"
      working-directory: client
      install-command: npm ci
      build-command: npm run build
      test-command: npm test
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `node-version` | `20` | Node.js version passed to `actions/setup-node`. |
| `working-directory` | `.` | Directory containing `package.json`. |
| `install-command` | `npm ci` | Dependency install command. |
| `build-command` | empty | Optional build command. Empty skips the build step. |
| `test-command` | empty | Optional test command. Empty skips the test step. |
| `cache` | `npm` | Cache mode passed to `actions/setup-node`. |

## Dependencies

- `actions/setup-node@v4`
- Bash shell
- A checked-out repository

## Related Reusable Workflow

Use `.github/workflows/reusable-node-ci.yml` when the caller wants the full job wrapper with checkout and optional artifact upload.
