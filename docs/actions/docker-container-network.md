# Docker Container Network

Composite action: `cobycloud/actions/actions/docker-container-network@main`

Idempotently attaches or detaches an existing container, such as Nginx Proxy Manager, from an application-specific Docker network. This enables Docker DNS upstreams without publishing application HTTP ports on the host.

```yaml
- uses: cobycloud/actions/actions/docker-container-network@main
  with:
    container: portwyrm-portwyrm-1
    network: tigrbl-wt-video-demo-network
    operation: attach
    aliases: npm-proxy
```

Use `operation: detach` to remove the attachment. Set `force: "true"` only when Docker requires forced detachment.

The action verifies that the container and network exist, skips an already-satisfied operation, and verifies the final attachment state.

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `container` | required | Existing container name or ID. |
| `network` | required | Existing Docker network name. |
| `operation` | `attach` | `attach` or `detach`. |
| `aliases` | empty | Optional comma-separated aliases for attachment. |
| `force` | `false` | Pass `--force` when detaching. |

Use `.github/workflows/reusable-docker-container-network.yml` when the caller wants runner selection, environment protection, and concurrency.