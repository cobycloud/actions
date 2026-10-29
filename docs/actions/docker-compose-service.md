# Docker Compose Service

Composite action: `cobycloud/actions/actions/docker-compose-service@main`

Restarts, rebuilds, or collects logs for one Docker Compose service.

## Use When

- A self-hosted deployment runner manages services with Docker Compose.
- Repeated workflows stop, remove, rebuild, and restart one service at a time.
- A workflow needs a standard log collection step for one service.

## Restart Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/docker-compose-service@main
    with:
      compose-command: docker compose
      service: backend
      operation: restart
```

## Logs Example

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/docker-compose-service@main
    with:
      service: backend
      operation: logs
      logs-output: backend.log
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `compose-command` | `docker compose` | Docker Compose executable, such as `docker compose` or `docker-compose`. |
| `compose-file` | empty | Optional compose file passed as `-f`. |
| `service` | required | Service name. |
| `operation` | `restart` | One of `restart`, `rebuild`, or `logs`. |
| `prune` | `false` | Deprecated compatibility input. Never enable it on a shared deployment host. |
| `logs-output` | `compose-service.log` | Output path for `logs` operation. |

## Dependencies

- Bash shell
- Docker
- Docker Compose
- A runner with access to the deployment environment

## Shared-host safety

Do not set `prune: "true"` on VM102, VM103, VM104, or another multi-tenant deployment host.
`docker system prune -af` is daemon-wide: one repository can delete build cache and unused images
owned by unrelated workloads. Use project-scoped Compose cleanup and normal Docker image-retention
operations instead. Mutating workflows must also hold the host's
[`host-mutation-lock`](host-mutation-lock.md) lease for their full mutation window.

## Related Reusable Workflow

Use `.github/workflows/reusable-docker-compose-service.yml` when the caller wants checkout, deployment runner selection, concurrency, and optional log artifact upload.
