# Homebrew Publish

`actions/brew-publish` checks out a Homebrew tap, runs a formula update command, and opens a pull request.

## Purpose

- Update formulae or casks in a Homebrew tap.
- Keep formula generation command caller-owned.
- Open a pull request rather than pushing directly to the tap default branch.

## Dependencies

- `actions/checkout`
- `peter-evans/create-pull-request`
- GitHub token with access to the tap repository

## Reusable Workflow

- `.github/workflows/reusable-brew-publish.yml`

## Example

```yaml
jobs:
  brew:
    uses: cobycloud/actions/.github/workflows/reusable-brew-publish.yml@main
    with:
      tap-repository: example/homebrew-tap
      update-command: ./update-formula.sh myapp 1.2.3
    secrets:
      TAP_GITHUB_TOKEN: ${{ secrets.TAP_GITHUB_TOKEN }}
```
