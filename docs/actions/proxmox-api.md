# Proxmox API actions

The typed Proxmox actions provide portable API mechanics without embedding hostnames, VM IDs, or organization policy.

## Authentication

Pass a PVE API token ID and secret from the caller's protected environment. Pass a CA certificate file and keep TLS verification enabled.

## Components

- `proxmox-api`: GET, POST, PUT, or DELETE against a caller-selected API path.
- `proxmox-task-wait`: poll an asynchronous UPID and fail on non-`OK` exit status.
- `proxmox-power`: start, gracefully shut down, or explicitly hard-stop a numeric VM ID.

The final workflow must own environment approval, concurrency, allowed VM IDs, and post-operation verification.
