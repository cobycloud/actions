# Proxmox Command

`actions/proxmox-command` is a low-level compatibility wrapper for caller-owned Terraform, Ansible, shell, or API tooling. New workflows should use the typed API, task-wait, and power actions.

## Purpose

- Normalize Proxmox plan/apply workflow shells.
- Keep Proxmox credentials, hostnames, and VM intent files out of the reusable action.
- Optionally upload plan/apply outputs for review or evidence.

## Typed alternatives

- `actions/proxmox-api`: one TLS-verified request with a PVE token and redacted failure behavior.
- `actions/proxmox-task-wait`: bounded polling of an asynchronous PVE UPID.
- `actions/proxmox-power`: validates VM ID and permits only start, graceful shutdown, or explicitly allowed hard stop.

The API actions require a CA file and never offer an insecure TLS switch.

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
