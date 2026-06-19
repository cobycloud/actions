# npm Publish

Composite action: `cobycloud/actions/actions/npm-publish@main`

Publishes a Node package to npmjs or another npm-compatible registry, with optional install, build, test, dist-tag, access, dry-run, provenance, token publishing, trusted publishing, and token-or-trusted fallback controls.

## Use When

- A package should be published to npmjs.
- The caller needs a reusable `npm publish` lane.
- Publication should use npm provenance.
- Publication should use `NPM_API_TOKEN`, npm trusted publishing, or trusted publishing when no token is supplied.

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
      publish-mode: auto
      npm-api-token: ${{ secrets.NPM_API_TOKEN }}
      tag: latest
      access: public
      provenance: "true"
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `publish-mode` | `auto` | `token` requires `npm-api-token`; `trusted` unsets npm token config and relies on npm trusted publishing; `auto` uses `npm-api-token` when present and otherwise uses trusted publishing. |
| `node-version` | `25` | Node.js version. Node 25 includes an npm version new enough for trusted publishing. |
| `package-directory` | `.` | Directory containing `package.json`. |
| `registry-url` | `https://registry.npmjs.org` | npm registry URL. |
| `scope` | empty | Optional package scope for registry setup. |
| `npm-api-token` | empty | Optional `NPM_API_TOKEN`. Required when `publish-mode` is `token`. |
| `install-command` | `npm ci` | Optional install command. Empty skips install. |
| `build-command` | empty | Optional build command. |
| `test-command` | empty | Optional test command. |
| `tag` | `latest` | npm dist-tag. |
| `access` | `public` | npm access level. Empty omits `--access`. |
| `provenance` | `true` | Adds `--provenance`. |
| `dry-run` | `false` | Adds `--dry-run`. |

## Dependencies

- `actions/setup-node@v4`
- npm token when `publish-mode` is `token`
- `id-token: write` when using provenance or npm trusted publishing

## Related Reusable Workflow

Use `.github/workflows/reusable-npm-publish.yml` for the full reusable job wrapper.

Reusable workflow secrets:

| Secret | Required | Description |
| --- | --- | --- |
| `NPM_API_TOKEN` | no | Optional npm automation token. Required only when `publish-mode` is `token`. |
