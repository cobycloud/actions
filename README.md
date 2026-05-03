# Reusable GitHub Actions

This repository turns repeated workflow patterns from the Swarmauri workspace into externally callable GitHub Actions and reusable workflows.

## Table of Contents

- [Action Catalog](#action-catalog)
- [Reusable Workflow Catalog](#reusable-workflow-catalog)
- [Component Analysis](#component-analysis)
- [Missing Workflow Families](#missing-workflow-families)
- [Source Analysis](#source-analysis)

## Documentation

| Document | Purpose |
| --- | --- |
| [`docs/reusable-component-map.md`](docs/reusable-component-map.md) | Component map from deduped workflow analysis to reusable action/workflow surfaces. |
| [`docs/missing-reusable-workflow-families.md`](docs/missing-reusable-workflow-families.md) | Expanded gap analysis for reusable workflow families not covered by the initial catalog. |
| [`docs/actions/setup-node-project.md`](docs/actions/setup-node-project.md) | Setup Node, install dependencies, and optionally run build/test commands. |
| [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build frontend dist output and commit changed generated files. |
| [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Set up Python with `uv`, install dependencies, compute optional monorepo `PYTHONPATH`, and run validation. |
| [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build Python package distributions with `uv build` and upload artifacts. |
| [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart, rebuild, or collect logs for one Docker Compose service. |

## Action Catalog

Use composite actions when a repository already owns its workflow shape and only wants to avoid repeated step blocks.

| Action | Documentation | Purpose |
| --- | --- | --- |
| [`./actions/setup-node-project`](actions/setup-node-project/action.yml) | [`docs/actions/setup-node-project.md`](docs/actions/setup-node-project.md) | Install Node dependencies and optionally run build/test commands in a package directory. |
| [`./actions/build-and-commit-dist`](actions/build-and-commit-dist/action.yml) | [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build a Node/Vite-style distribution folder and commit generated output when it changes. |
| [`./actions/python-uv`](actions/python-uv/action.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Set up Python with `uv`, install dependencies, optionally compute monorepo `PYTHONPATH`, and run a validation command. |
| [`./actions/python-package-build`](actions/python-package-build/action.yml) | [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build Python packages with `uv build` and optionally upload distribution artifacts. |
| [`./actions/docker-compose-service`](actions/docker-compose-service/action.yml) | [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart, rebuild, or collect logs for one Docker Compose service. |

External use example:

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: cobycloud/actions/actions/python-uv@main
    with:
      python-version: "3.12"
      working-directory: backend
      install-command: uv pip install -e . pytest
      run-command: uv run pytest
```

## Reusable Workflow Catalog

Use reusable workflows when a repository wants the full job wrapper.

| Workflow | Related Action Doc | Purpose |
| --- | --- | --- |
| [`.github/workflows/reusable-node-ci.yml`](.github/workflows/reusable-node-ci.yml) | [`docs/actions/setup-node-project.md`](docs/actions/setup-node-project.md) | Checkout, Node setup, install, build, test, and optional artifact upload. |
| [`.github/workflows/reusable-build-and-commit-dist.yml`](.github/workflows/reusable-build-and-commit-dist.yml) | [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build a frontend distribution directory and commit it back to the branch. |
| [`.github/workflows/reusable-python-uv-ci.yml`](.github/workflows/reusable-python-uv-ci.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Checkout, Python/uv setup, dependency install, optional monorepo `PYTHONPATH`, validation command, and optional artifact upload. |
| [`.github/workflows/reusable-python-package-build.yml`](.github/workflows/reusable-python-package-build.yml) | [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build one Python package and upload its `dist` output. |
| [`.github/workflows/reusable-docker-compose-service.yml`](.github/workflows/reusable-docker-compose-service.yml) | [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart/rebuild/log a Docker Compose service from a deployment runner. |

External use example:

```yaml
jobs:
  python:
    uses: cobycloud/actions/.github/workflows/reusable-python-uv-ci.yml@main
    with:
      working-directory: backend
      install-command: uv pip install -e . pytest
      run-command: uv run pytest
```

## Component Analysis

Start with [`docs/reusable-component-map.md`](docs/reusable-component-map.md) for the action-level design and deferred extraction candidates.

## Missing Workflow Families

The initial reusable set does not yet cover package publication, Rust/Cargo, npmjs, crates.io, PyPI, GitHub Releases, license scans, dependency review, metadata checks, version bumps, monorepo/set-based work, Terraform, Proxmox, Playwright/e2e, git automation, docs deployment, provenance, signing, test matrices, platform artifacts, or apt/snap/brew publication. See [`docs/missing-reusable-workflow-families.md`](docs/missing-reusable-workflow-families.md).

## Source Analysis

The first reusable set is grounded in the generated inventory under `reports/`:

- [`reports/workflow-inventory.md`](reports/workflow-inventory.md)
- [`reports/final-workflow-component-analysis.md`](reports/final-workflow-component-analysis.md)
- [`reports/workflows/`](reports/workflows/)
- [`reports/scripts/`](reports/scripts/)

The copied historical workflows remain under `.github/workflows/*__<hash>.yml` for reference. New reusable workflows use the `reusable-*.yml` naming convention.
