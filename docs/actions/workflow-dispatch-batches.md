# Workflow Dispatch Batches

`actions/workflow-dispatch-batches` dispatches child workflows from a JSON batch list.

## Purpose

- Trigger batch workflows from a parent orchestration workflow.
- Pass per-batch workflow inputs.
- Support monorepo package or release train fan-out when a matrix is not enough.

## Reusable Workflow

- `.github/workflows/reusable-workflow-dispatch-batches.yml`

## Example

```yaml
jobs:
  dispatch:
    uses: cobycloud/actions/.github/workflows/reusable-workflow-dispatch-batches.yml@main
    with:
      batches-json: >-
        [
          {"workflow":"package-ci.yml","ref":"main","inputs":{"package":"core"}}
        ]
    secrets:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
