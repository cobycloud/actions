# Terraform Plan

`actions/terraform-plan` sets up Terraform, runs init/validate/plan, and uploads the generated plan artifact.

## Purpose

- Standardize Terraform pre-apply gates.
- Preserve a binary or text plan artifact for review or downstream apply jobs.
- Keep backend/provider credentials owned by the caller workflow environment.

## Dependencies

- `hashicorp/setup-terraform`
- `actions/upload-artifact`
- Terraform configuration in the caller repository

## Reusable Workflow

- `.github/workflows/reusable-terraform-plan.yml`

## Example

```yaml
jobs:
  plan:
    uses: cobycloud/actions/.github/workflows/reusable-terraform-plan.yml@main
    with:
      working-directory: infra/prod
      plan-command: terraform plan -out=tfplan
```
