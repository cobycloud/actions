# Terraform Plan

`actions/terraform-plan` sets up Terraform, runs init/validate/plan, and uploads the generated binary plan with immutable provenance metadata.

## Purpose

- Standardize Terraform pre-apply gates.
- Preserve a binary plan and metadata containing its SHA-256, source commit, provider lock checksum, and Terraform version.
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

Pass the emitted `plan-sha256` and `source-sha` outputs to the separately approved apply job. Artifacts are retained for 14 days by default.
