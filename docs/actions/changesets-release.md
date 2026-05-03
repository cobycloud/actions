# Changesets Release

Composite action: `cobycloud/actions/actions/changesets-release@main`

Runs `changesets/action` to create a version PR or publish packages from a Changesets-managed Node monorepo.

## Use When

- A repository uses Changesets for versioning and changelog generation.
- A release workflow should either create a version PR or publish packages when changesets are ready.
- npm publication should share the same reusable release lane.

## Example

```yaml
permissions:
  contents: write
  pull-requests: write
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/changesets-release@main
    with:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      npm-token: ${{ secrets.NPM_TOKEN }}
      version-command: npx changeset version
      publish-command: npx changeset publish
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `node-version` | `20` | Node.js version. |
| `package-directory` | `.` | Directory containing Changesets config and package manifests. |
| `github-token` | required | GitHub token used by `changesets/action`. |
| `npm-token` | empty | Optional npm token for publish commands. |
| `version-command` | `npx changeset version` | Command that versions packages and changelogs. |
| `publish-command` | `npx changeset publish` | Command that publishes packages. |
| `commit` | `chore: version packages` | Version PR commit message. |
| `title` | `chore: version packages` | Version PR title. |
| `create-github-releases` | `false` | Ask `changesets/action` to create GitHub Releases. |

## Outputs

| Output | Description |
| --- | --- |
| `published` | Whether packages were published. |
| `published-packages` | Published packages JSON from `changesets/action`. |
| `pull-request-number` | Version PR number from `changesets/action`. |

## Related Reusable Workflow

Use `.github/workflows/reusable-changesets-release.yml` for the full reusable job wrapper.
