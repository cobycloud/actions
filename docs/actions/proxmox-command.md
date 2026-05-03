# Proxmox Command

`actions/proxmox-command` runs Proxmox plan or apply commands through caller-owned Terraform, Ansible, shell, or API tooling.

## Purpose

- Normalize Proxmox plan/apply workflow shells.
- Keep Proxmox credentials, hostnames, and VM intent files out of the reusable action.
- Optionally upload plan/apply outputs for review or evidence.

## Dependencies

- Caller-provided Proxmox tooling installed by `setup-command` or already available on the runner.
- `actions/upload-artifact` when output upload is enabled.

## Reusable Workflows

- `.github/workflows/reusable-proxmox-plan.yml`
- `.github/workflows/reusable-proxmox-apply.yml`

## Example

```yaml
jobs:
  proxmox-plan:
    uses: cobycloud/actions/.github/workflows/reusable-proxmox-plan.yml@main
    with:
      working-directory: infra/proxmox
      plan-command: ./scripts/proxmox-plan.sh
      upload-artifact-path: plan.json
```
