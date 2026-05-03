# Reusable Component Map

This map converts the workflow inventory into reusable external surfaces. It intentionally starts with high-repeat, low-domain-specific components rather than copying repo-specific release gates verbatim.

## Components

### Node Project CI

- Action: `actions/setup-node-project`
- Workflow: `.github/workflows/reusable-node-ci.yml`
- Replaces repeated jobs that run `actions/setup-node`, `npm ci`, `npm run build`, and `npm test`.
- Main inputs: `node-version`, `working-directory`, `install-command`, `build-command`, `test-command`.
- Domain fit: frontend clients, docs apps, Vite/React apps, Node package validation.

### Build and Commit Dist

- Action: `actions/build-and-commit-dist`
- Workflow: `.github/workflows/reusable-build-and-commit-dist.yml`
- Replaces repeated jobs that build `client/dist` or equivalent generated frontend output and push a bot commit.
- Main inputs: `working-directory`, `install-command`, `build-command`, `dist-path`, `commit-message`.
- Required permission: `contents: write`.
- Domain fit: static clients where generated distribution output is committed.

### Python uv CI

- Action: `actions/python-uv`
- Workflow: `.github/workflows/reusable-python-uv-ci.yml`
- Replaces repeated jobs that set up Python, install `uv`, install dependencies, compute workspace `PYTHONPATH`, and run `pytest` or repo-local validation commands.
- Main inputs: `python-version`, `working-directory`, `install-command`, `run-command`, `compute-monorepo-pythonpath`.
- Domain fit: Python packages, uv workspaces, Swarmauri/Tigrbl package trees, SSOT validation gates.

### Python Package Build

- Action: `actions/python-package-build`
- Workflow: `.github/workflows/reusable-python-package-build.yml`
- Replaces repeated jobs that call `uv build` for one package and upload the resulting distributions.
- Main inputs: `project-path`, `out-dir`, `artifact-name`.
- Domain fit: PyPI package build lanes and release smoke lanes.

### Docker Compose Service

- Action: `actions/docker-compose-service`
- Workflow: `.github/workflows/reusable-docker-compose-service.yml`
- Replaces repeated deployment-runner jobs that stop, remove, prune, rebuild, and restart a single Compose service, or collect service logs.
- Main inputs: `compose-command`, `compose-file`, `service`, `operation`, `prune`, `logs-output`.
- Domain fit: self-hosted deployment runners and app stacks with client/backend/relay/minio service lanes.

## Deferred Components

These were visible in the inventory but are intentionally deferred until their contracts are normalized:

- SSOT release/certification gates: high-value, but repo-specific command paths and registry assumptions vary.
- Tigrbl/tigrbl_auth proof lanes: reusable workflow candidates, but they need a stable evidence contract before extraction.
- Multi-package release trains: useful for `ssot-registry` and SDK-style repos, but they need a matrix manifest input rather than hard-coded package lists.
- Cloud deployment docs lanes: similar shape, but each current workflow embeds provider-specific secrets and hosting targets.

See `docs/missing-reusable-workflow-families.md` for the expanded gap list covering package publication, Rust/Cargo, npmjs, crates.io, PyPI, GitHub Releases, license and dependency review, metadata checks, version bumps, monorepo/set-based work, Terraform, Proxmox, Playwright/e2e, git automation, docs deployment, provenance, signing, matrices, platform artifacts, and package-manager publication.
