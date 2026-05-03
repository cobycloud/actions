# Playwright CI

`actions/playwright-ci` installs Node dependencies, installs Playwright browsers, runs e2e tests, and uploads report, trace, screenshot, and video outputs.

## Purpose

- Standardize browser e2e lanes across frontend repositories.
- Keep install and test commands configurable for npm, pnpm, yarn, and monorepo layouts.
- Preserve Playwright reports and `test-results` artifacts for failed runs.

## Dependencies

- `actions/setup-node`
- `actions/upload-artifact`
- Playwright installed by the target repository
- Browser dependencies installed through `npx playwright install --with-deps` by default

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `node-version` | `20` | Node.js version to install. |
| `working-directory` | `.` | Directory containing the Playwright project. |
| `install-command` | `npm ci` | Dependency install command. |
| `browser-install-command` | `npx playwright install --with-deps` | Browser install command. |
| `test-command` | `npx playwright test` | E2E command. |
| `upload-artifacts` | `true` | Upload report and result artifacts. |
| `report-path` | `playwright-report` | HTML report path. |
| `results-path` | `test-results` | Trace/screenshot/video result path. |

## Reusable Workflow

- `.github/workflows/reusable-playwright.yml`

## Example

```yaml
jobs:
  e2e:
    uses: cobycloud/actions/.github/workflows/reusable-playwright.yml@main
    with:
      working-directory: apps/client
      test-command: npx playwright test --project=chromium
```
