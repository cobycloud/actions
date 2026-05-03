# Terraform Apply

`actions/terraform-apply` sets up Terraform and runs a caller-provided apply command, optionally after downloading a plan artifact.

## Purpose

- Separate apply from plan so repositories can put apply behind environments and approvals.
- Support applying a downloaded plan artifact or a direct apply command.
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
```
