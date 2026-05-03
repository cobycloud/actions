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
      prune: "true"
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
| `prune` | `false` | Runs `docker system prune -af` before rebuild/restart when true. |
| `logs-output` | `compose-service.log` | Output path for `logs` operation. |

## Dependencies

- Bash shell
- Docker
- Docker Compose
- A runner with access to the deployment environment

## Related Reusable Workflow

Use `.github/workflows/reusable-docker-compose-service.yml` when the caller wants checkout, deployment runner selection, concurrency, and optional log artifact upload.
