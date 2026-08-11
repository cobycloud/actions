# Terraform Apply

`actions/terraform-apply` downloads, verifies, and applies a previously reviewed binary plan.

## Purpose

- Separate apply from plan so repositories can put apply behind environments and approvals.
- Reject plans whose SHA-256 or source commit differs from the approved values.
- Keep cloud credentials and backend configuration caller-owned.

## Dependencies

- `hashicorp/setup-terraform`
- `actions/download-artifact`
- Terraform configuration in the caller repository

## Reusable Workflow

- `.github/workflows/reusable-terraform-apply.yml`

## Example

```yaml
jobs:
  apply:
    uses: cobycloud/actions/.github/workflows/reusable-terraform-apply.yml@main
    with:
      environment: production
      working-directory: infra/prod
      plan-artifact-name: terraform-plan
      apply-command: terraform apply -auto-approve tfplan
      expected-source-sha: ${{ needs.plan.outputs.source-sha }}
      expected-plan-sha256: ${{ needs.plan.outputs.plan-sha256 }}
      plan-run-id: ${{ inputs.plan_run_id }}
      github-token: ${{ github.token }}
```

Set `plan-run-id` and provide a token with `actions:read` when apply is intentionally dispatched as a separate workflow run.
