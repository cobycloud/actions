# npm Publish

Composite action: `cobycloud/actions/actions/npm-publish@main`

Publishes a Node package to npmjs or another npm-compatible registry, with optional install, build, test, dist-tag, access, dry-run, and provenance controls.

## Use When

- A package should be published to npmjs.
- The caller needs a reusable `npm publish` lane.
- Publication should use npm provenance.

## Example

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/npm-publish@main
    with:
      package-directory: packages/example
      npm-token: ${{ secrets.NPM_TOKEN }}
      tag: latest
      access: public
      provenance: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `node-version` | `20` | Node.js version. |
| `package-directory` | `.` | Directory containing `package.json`. |
| `registry-url` | `https://registry.npmjs.org` | npm registry URL. |
| `scope` | empty | Optional package scope for registry setup. |
| `npm-token` | required | npm automation token. |
| `install-command` | `npm ci` | Optional install command. Empty skips install. |
| `build-command` | empty | Optional build command. |
| `test-command` | empty | Optional test command. |
| `tag` | `latest` | npm dist-tag. |
| `access` | `public` | npm access level. Empty omits `--access`. |
| `provenance` | `true` | Adds `--provenance`. |
| `dry-run` | `false` | Adds `--dry-run`. |

## Dependencies

- `actions/setup-node@v4`
- npm token
- `id-token: write` when using provenance

## Related Reusable Workflow

Use `.github/workflows/reusable-npm-publish.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `NPM_TOKEN` | yes | npm automation token. |
