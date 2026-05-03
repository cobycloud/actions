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
| [`docs/actions/node-lint-typecheck.md`](docs/actions/node-lint-typecheck.md) | Set up Node and run lint, typecheck, test, and build checks. |
| [`docs/actions/js-framework-ci.md`](docs/actions/js-framework-ci.md) | Run Vite, Svelte, Vue, React, or generic frontend CI checks. |
| [`docs/actions/playwright-ci.md`](docs/actions/playwright-ci.md) | Run Playwright e2e tests and upload reports, traces, screenshots, and videos. |
| [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build frontend dist output and commit changed generated files. |
| [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Set up Python with `uv`, install dependencies, compute optional monorepo `PYTHONPATH`, and run validation. |
| [`docs/actions/tox-ci.md`](docs/actions/tox-ci.md) | Set up Python, install tox, and run tox environments. |
| [`docs/actions/python-package-ci.md`](docs/actions/python-package-ci.md) | Run Python package compile, test, docs, build, and artifact checks across package cells. |
| [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build Python package distributions with `uv build` and upload artifacts. |
| [`docs/actions/rust-cargo-ci.md`](docs/actions/rust-cargo-ci.md) | Set up Rust and run Cargo fmt, clippy, test, build, and docs checks. |
| [`docs/actions/os-matrix-cell.md`](docs/actions/os-matrix-cell.md) | Run one Node, Python, Rust, or generic validation cell on the current runner OS. |
| [`docs/actions/cross-platform-command.md`](docs/actions/cross-platform-command.md) | Run default commands with Linux, macOS, and Windows overrides. |
| [`docs/actions/platform-artifact-build.md`](docs/actions/platform-artifact-build.md) | Build Linux, Windows, or Darwin artifacts and upload outputs. |
| [`docs/actions/android-artifact-build.md`](docs/actions/android-artifact-build.md) | Build Android APK/AAB artifacts and upload outputs. |
| [`docs/actions/electron-artifact-build.md`](docs/actions/electron-artifact-build.md) | Build Electron desktop installers and upload outputs. |
| [`docs/actions/tauri-artifact-build.md`](docs/actions/tauri-artifact-build.md) | Build Tauri desktop bundles and upload outputs. |
| [`docs/actions/deb-package-build.md`](docs/actions/deb-package-build.md) | Build Debian packages and upload `.deb` outputs. |
| [`docs/actions/snap-build.md`](docs/actions/snap-build.md) | Build Snap packages and upload `.snap` outputs. |
| [`docs/actions/apt-publish.md`](docs/actions/apt-publish.md) | Publish Debian packages to an APT repository using caller-owned tooling. |
| [`docs/actions/rpm-publish.md`](docs/actions/rpm-publish.md) | Publish RPM packages to a YUM/DNF repository using caller-owned tooling. |
| [`docs/actions/snap-publish.md`](docs/actions/snap-publish.md) | Publish Snap packages to Snapcraft. |
| [`docs/actions/brew-publish.md`](docs/actions/brew-publish.md) | Update Homebrew formulae or casks in a tap repository. |
| [`docs/actions/linux-package-publish.md`](docs/actions/linux-package-publish.md) | Route package publication across APT, RPM, Snapcraft, and Homebrew lanes. |
| [`docs/actions/terraform-plan.md`](docs/actions/terraform-plan.md) | Run Terraform init, validate, plan, and upload the plan artifact. |
| [`docs/actions/terraform-apply.md`](docs/actions/terraform-apply.md) | Run Terraform apply with optional plan artifact download. |
| [`docs/actions/proxmox-command.md`](docs/actions/proxmox-command.md) | Run Proxmox plan/apply commands through caller-owned tooling. |
| [`docs/actions/docs-build.md`](docs/actions/docs-build.md) | Build documentation and upload generated site artifacts. |
| [`docs/actions/pages-deploy.md`](docs/actions/pages-deploy.md) | Upload and deploy GitHub Pages artifacts. |
| [`docs/actions/static-app-build.md`](docs/actions/static-app-build.md) | Build static apps and upload generated output. |
| [`docs/actions/static-app-deploy.md`](docs/actions/static-app-deploy.md) | Deploy static apps with caller-owned provider commands. |
| [`docs/actions/cloudflare-pages-deploy.md`](docs/actions/cloudflare-pages-deploy.md) | Deploy static apps to Cloudflare Pages. |
| [`docs/actions/netlify-deploy.md`](docs/actions/netlify-deploy.md) | Deploy static apps to Netlify. |
| [`docs/actions/vercel-deploy.md`](docs/actions/vercel-deploy.md) | Deploy static apps to Vercel. |
| [`docs/actions/monorepo-discover.md`](docs/actions/monorepo-discover.md) | Discover monorepo package cells and generate matrix JSON. |
| [`docs/actions/uv-monorepo-ci.md`](docs/actions/uv-monorepo-ci.md) | Run uv-based monorepo package CI cells. |
| [`docs/actions/pnpm-monorepo-ci.md`](docs/actions/pnpm-monorepo-ci.md) | Run pnpm-based monorepo package CI cells. |
| [`docs/actions/monorepo-release-train.md`](docs/actions/monorepo-release-train.md) | Execute ordered commands across package cells. |
| [`docs/actions/monorepo-artifact-join.md`](docs/actions/monorepo-artifact-join.md) | Join matrix artifacts and verify aggregate output. |
| [`docs/actions/changed-files.md`](docs/actions/changed-files.md) | Detect changed files and derive changed package cells. |
| [`docs/actions/git-commit-generated.md`](docs/actions/git-commit-generated.md) | Commit generated outputs without assuming a specific artifact path. |
| [`docs/actions/create-pr.md`](docs/actions/create-pr.md) | Create or update a pull request for generated changes. |
| [`docs/actions/sync-docs.md`](docs/actions/sync-docs.md) | Sync generated docs and open a pull request. |
| [`docs/actions/workflow-dispatch-batches.md`](docs/actions/workflow-dispatch-batches.md) | Dispatch child workflows from JSON batch definitions. |
| [`docs/actions/ssot-validate.md`](docs/actions/ssot-validate.md) | Validate SSOT registries and upload validation reports. |
| [`docs/actions/ssot-sync-statuses.md`](docs/actions/ssot-sync-statuses.md) | Synchronize SSOT implementation status from evidence or repo truth. |
| [`docs/actions/ssot-boundary-gate.md`](docs/actions/ssot-boundary-gate.md) | Gate work on SSOT boundary scope and frozen readiness. |
| [`docs/actions/ssot-evidence-lane.md`](docs/actions/ssot-evidence-lane.md) | Run SSOT evidence lanes and upload evidence artifacts. |
| [`docs/actions/ssot-certification-profile.md`](docs/actions/ssot-certification-profile.md) | Run SSOT certification profile checks. |
| [`docs/actions/ssot-release-certify.md`](docs/actions/ssot-release-certify.md) | Certify, promote, or publish SSOT release entities. |
| [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart, rebuild, or collect logs for one Docker Compose service. |
| [`docs/actions/pypi-publish.md`](docs/actions/pypi-publish.md) | Publish Python distributions to PyPI or TestPyPI. |
| [`docs/actions/npm-publish.md`](docs/actions/npm-publish.md) | Publish Node packages to npmjs or another npm-compatible registry. |
| [`docs/actions/crates-publish.md`](docs/actions/crates-publish.md) | Publish Rust crates with `cargo publish`. |
| [`docs/actions/github-release.md`](docs/actions/github-release.md) | Create or update GitHub Releases and upload files. |
| [`docs/actions/release-assets.md`](docs/actions/release-assets.md) | Download artifacts, normalize release assets, and generate checksums. |
| [`docs/actions/version-bump.md`](docs/actions/version-bump.md) | Bump versions in package manifests, TOML files, and release metadata. |
| [`docs/actions/release-prepare.md`](docs/actions/release-prepare.md) | Compute release tag/name and generate release notes from changelog content. |
| [`docs/actions/changesets-release.md`](docs/actions/changesets-release.md) | Create Changesets version PRs or publish Changesets-managed packages. |
| [`docs/actions/license-scan.md`](docs/actions/license-scan.md) | Scan package manifests for license declarations and license file coverage. |
| [`docs/actions/package-metadata.md`](docs/actions/package-metadata.md) | Validate package manifest names, versions, descriptions, licenses, readmes, and URLs. |
| [`docs/actions/notice-readme-check.md`](docs/actions/notice-readme-check.md) | Verify README, NOTICE, LICENSE, and package-name consistency. |
| [`docs/actions/toml-validate.md`](docs/actions/toml-validate.md) | Validate TOML syntax and required package metadata sections. |
| [`docs/actions/codeql.md`](docs/actions/codeql.md) | Run CodeQL init, optional autobuild, and analyze. |
| [`docs/actions/dependency-review.md`](docs/actions/dependency-review.md) | Run GitHub dependency review with reusable policy inputs. |
| [`docs/actions/security-gate.md`](docs/actions/security-gate.md) | Aggregate license, metadata, TOML, dependency review, and CodeQL checks. |
| [`docs/actions/artifact-attestation.md`](docs/actions/artifact-attestation.md) | Generate build provenance attestations for artifact paths. |
| [`docs/actions/release-attestation.md`](docs/actions/release-attestation.md) | Generate provenance attestations for release asset files. |
| [`docs/actions/sign-artifacts.md`](docs/actions/sign-artifacts.md) | Sign files with cosign keyless or key-based signing. |
| [`docs/actions/verify-attestations.md`](docs/actions/verify-attestations.md) | Verify GitHub artifact attestations and optional cosign signatures. |

## Action Catalog

Use composite actions when a repository already owns its workflow shape and only wants to avoid repeated step blocks.

| Action | Documentation | Purpose |
| --- | --- | --- |
| [`./actions/setup-node-project`](actions/setup-node-project/action.yml) | [`docs/actions/setup-node-project.md`](docs/actions/setup-node-project.md) | Install Node dependencies and optionally run build/test commands in a package directory. |
| [`./actions/node-lint-typecheck`](actions/node-lint-typecheck/action.yml) | [`docs/actions/node-lint-typecheck.md`](docs/actions/node-lint-typecheck.md) | Set up Node and run lint, typecheck, test, and build checks. |
| [`./actions/js-framework-ci`](actions/js-framework-ci/action.yml) | [`docs/actions/js-framework-ci.md`](docs/actions/js-framework-ci.md) | Run Vite, Svelte, Vue, React, or generic frontend CI checks. |
| [`./actions/playwright-ci`](actions/playwright-ci/action.yml) | [`docs/actions/playwright-ci.md`](docs/actions/playwright-ci.md) | Run Playwright e2e tests and upload reports, traces, screenshots, and videos. |
| [`./actions/build-and-commit-dist`](actions/build-and-commit-dist/action.yml) | [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build a Node/Vite-style distribution folder and commit generated output when it changes. |
| [`./actions/python-uv`](actions/python-uv/action.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Set up Python with `uv`, install dependencies, optionally compute monorepo `PYTHONPATH`, and run a validation command. |
| [`./actions/tox-ci`](actions/tox-ci/action.yml) | [`docs/actions/tox-ci.md`](docs/actions/tox-ci.md) | Set up Python, install tox, and run tox environments. |
| [`./actions/python-package-ci`](actions/python-package-ci/action.yml) | [`docs/actions/python-package-ci.md`](docs/actions/python-package-ci.md) | Run Python package compile, test, docs, build, and artifact checks across package cells. |
| [`./actions/python-package-build`](actions/python-package-build/action.yml) | [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build Python packages with `uv build` and optionally upload distribution artifacts. |
| [`./actions/rust-cargo-ci`](actions/rust-cargo-ci/action.yml) | [`docs/actions/rust-cargo-ci.md`](docs/actions/rust-cargo-ci.md) | Set up Rust and run Cargo fmt, clippy, test, build, and docs checks. |
| [`./actions/os-matrix-cell`](actions/os-matrix-cell/action.yml) | [`docs/actions/os-matrix-cell.md`](docs/actions/os-matrix-cell.md) | Run one Node, Python, Rust, or generic validation cell on the current runner OS. |
| [`./actions/cross-platform-command`](actions/cross-platform-command/action.yml) | [`docs/actions/cross-platform-command.md`](docs/actions/cross-platform-command.md) | Run default commands with Linux, macOS, and Windows overrides. |
| [`./actions/platform-artifact-build`](actions/platform-artifact-build/action.yml) | [`docs/actions/platform-artifact-build.md`](docs/actions/platform-artifact-build.md) | Build Linux, Windows, or Darwin artifacts and upload outputs. |
| [`./actions/android-artifact-build`](actions/android-artifact-build/action.yml) | [`docs/actions/android-artifact-build.md`](docs/actions/android-artifact-build.md) | Build Android APK/AAB artifacts and upload outputs. |
| [`./actions/electron-artifact-build`](actions/electron-artifact-build/action.yml) | [`docs/actions/electron-artifact-build.md`](docs/actions/electron-artifact-build.md) | Build Electron desktop installers and upload outputs. |
| [`./actions/tauri-artifact-build`](actions/tauri-artifact-build/action.yml) | [`docs/actions/tauri-artifact-build.md`](docs/actions/tauri-artifact-build.md) | Build Tauri desktop bundles and upload outputs. |
| [`./actions/deb-package-build`](actions/deb-package-build/action.yml) | [`docs/actions/deb-package-build.md`](docs/actions/deb-package-build.md) | Build Debian packages and upload `.deb` outputs. |
| [`./actions/snap-build`](actions/snap-build/action.yml) | [`docs/actions/snap-build.md`](docs/actions/snap-build.md) | Build Snap packages and upload `.snap` outputs. |
| [`./actions/apt-publish`](actions/apt-publish/action.yml) | [`docs/actions/apt-publish.md`](docs/actions/apt-publish.md) | Publish Debian packages to an APT repository using caller-owned tooling. |
| [`./actions/rpm-publish`](actions/rpm-publish/action.yml) | [`docs/actions/rpm-publish.md`](docs/actions/rpm-publish.md) | Publish RPM packages to a YUM/DNF repository using caller-owned tooling. |
| [`./actions/snap-publish`](actions/snap-publish/action.yml) | [`docs/actions/snap-publish.md`](docs/actions/snap-publish.md) | Publish Snap packages to Snapcraft. |
| [`./actions/brew-publish`](actions/brew-publish/action.yml) | [`docs/actions/brew-publish.md`](docs/actions/brew-publish.md) | Update Homebrew formulae or casks in a tap repository. |
| [`./actions/terraform-plan`](actions/terraform-plan/action.yml) | [`docs/actions/terraform-plan.md`](docs/actions/terraform-plan.md) | Run Terraform init, validate, plan, and upload the plan artifact. |
| [`./actions/terraform-apply`](actions/terraform-apply/action.yml) | [`docs/actions/terraform-apply.md`](docs/actions/terraform-apply.md) | Run Terraform apply with optional plan artifact download. |
| [`./actions/proxmox-command`](actions/proxmox-command/action.yml) | [`docs/actions/proxmox-command.md`](docs/actions/proxmox-command.md) | Run Proxmox plan/apply commands through caller-owned tooling. |
| [`./actions/docs-build`](actions/docs-build/action.yml) | [`docs/actions/docs-build.md`](docs/actions/docs-build.md) | Build documentation and upload generated site artifacts. |
| [`./actions/pages-deploy`](actions/pages-deploy/action.yml) | [`docs/actions/pages-deploy.md`](docs/actions/pages-deploy.md) | Upload and deploy GitHub Pages artifacts. |
| [`./actions/static-app-build`](actions/static-app-build/action.yml) | [`docs/actions/static-app-build.md`](docs/actions/static-app-build.md) | Build static apps and upload generated output. |
| [`./actions/static-app-deploy`](actions/static-app-deploy/action.yml) | [`docs/actions/static-app-deploy.md`](docs/actions/static-app-deploy.md) | Deploy static apps with caller-owned provider commands. |
| [`./actions/cloudflare-pages-deploy`](actions/cloudflare-pages-deploy/action.yml) | [`docs/actions/cloudflare-pages-deploy.md`](docs/actions/cloudflare-pages-deploy.md) | Deploy static apps to Cloudflare Pages. |
| [`./actions/netlify-deploy`](actions/netlify-deploy/action.yml) | [`docs/actions/netlify-deploy.md`](docs/actions/netlify-deploy.md) | Deploy static apps to Netlify. |
| [`./actions/vercel-deploy`](actions/vercel-deploy/action.yml) | [`docs/actions/vercel-deploy.md`](docs/actions/vercel-deploy.md) | Deploy static apps to Vercel. |
| [`./actions/monorepo-discover`](actions/monorepo-discover/action.yml) | [`docs/actions/monorepo-discover.md`](docs/actions/monorepo-discover.md) | Discover monorepo package cells and generate matrix JSON. |
| [`./actions/uv-monorepo-ci`](actions/uv-monorepo-ci/action.yml) | [`docs/actions/uv-monorepo-ci.md`](docs/actions/uv-monorepo-ci.md) | Run uv-based monorepo package CI cells. |
| [`./actions/pnpm-monorepo-ci`](actions/pnpm-monorepo-ci/action.yml) | [`docs/actions/pnpm-monorepo-ci.md`](docs/actions/pnpm-monorepo-ci.md) | Run pnpm-based monorepo package CI cells. |
| [`./actions/monorepo-release-train`](actions/monorepo-release-train/action.yml) | [`docs/actions/monorepo-release-train.md`](docs/actions/monorepo-release-train.md) | Execute ordered commands across package cells. |
| [`./actions/monorepo-artifact-join`](actions/monorepo-artifact-join/action.yml) | [`docs/actions/monorepo-artifact-join.md`](docs/actions/monorepo-artifact-join.md) | Join matrix artifacts and verify aggregate output. |
| [`./actions/changed-files`](actions/changed-files/action.yml) | [`docs/actions/changed-files.md`](docs/actions/changed-files.md) | Detect changed files and derive changed package cells. |
| [`./actions/git-commit-generated`](actions/git-commit-generated/action.yml) | [`docs/actions/git-commit-generated.md`](docs/actions/git-commit-generated.md) | Commit generated outputs without assuming a specific artifact path. |
| [`./actions/create-pr`](actions/create-pr/action.yml) | [`docs/actions/create-pr.md`](docs/actions/create-pr.md) | Create or update a pull request for generated changes. |
| [`./actions/sync-docs`](actions/sync-docs/action.yml) | [`docs/actions/sync-docs.md`](docs/actions/sync-docs.md) | Sync generated docs and open a pull request. |
| [`./actions/workflow-dispatch-batches`](actions/workflow-dispatch-batches/action.yml) | [`docs/actions/workflow-dispatch-batches.md`](docs/actions/workflow-dispatch-batches.md) | Dispatch child workflows from JSON batch definitions. |
| [`./actions/ssot-validate`](actions/ssot-validate/action.yml) | [`docs/actions/ssot-validate.md`](docs/actions/ssot-validate.md) | Validate SSOT registries and upload validation reports. |
| [`./actions/ssot-sync-statuses`](actions/ssot-sync-statuses/action.yml) | [`docs/actions/ssot-sync-statuses.md`](docs/actions/ssot-sync-statuses.md) | Synchronize SSOT implementation status from evidence or repo truth. |
| [`./actions/ssot-boundary-gate`](actions/ssot-boundary-gate/action.yml) | [`docs/actions/ssot-boundary-gate.md`](docs/actions/ssot-boundary-gate.md) | Gate work on SSOT boundary scope and frozen readiness. |
| [`./actions/ssot-evidence-lane`](actions/ssot-evidence-lane/action.yml) | [`docs/actions/ssot-evidence-lane.md`](docs/actions/ssot-evidence-lane.md) | Run SSOT evidence lanes and upload evidence artifacts. |
| [`./actions/ssot-certification-profile`](actions/ssot-certification-profile/action.yml) | [`docs/actions/ssot-certification-profile.md`](docs/actions/ssot-certification-profile.md) | Run SSOT certification profile checks. |
| [`./actions/ssot-release-certify`](actions/ssot-release-certify/action.yml) | [`docs/actions/ssot-release-certify.md`](docs/actions/ssot-release-certify.md) | Certify, promote, or publish SSOT release entities. |
| [`./actions/docker-compose-service`](actions/docker-compose-service/action.yml) | [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart, rebuild, or collect logs for one Docker Compose service. |
| [`./actions/pypi-publish`](actions/pypi-publish/action.yml) | [`docs/actions/pypi-publish.md`](docs/actions/pypi-publish.md) | Publish Python distributions to PyPI or TestPyPI. |
| [`./actions/npm-publish`](actions/npm-publish/action.yml) | [`docs/actions/npm-publish.md`](docs/actions/npm-publish.md) | Publish Node packages to npmjs or another npm-compatible registry. |
| [`./actions/crates-publish`](actions/crates-publish/action.yml) | [`docs/actions/crates-publish.md`](docs/actions/crates-publish.md) | Publish Rust crates with `cargo publish`. |
| [`./actions/github-release`](actions/github-release/action.yml) | [`docs/actions/github-release.md`](docs/actions/github-release.md) | Create or update GitHub Releases and upload files. |
| [`./actions/release-assets`](actions/release-assets/action.yml) | [`docs/actions/release-assets.md`](docs/actions/release-assets.md) | Download artifacts, normalize release assets, and generate checksums. |
| [`./actions/version-bump`](actions/version-bump/action.yml) | [`docs/actions/version-bump.md`](docs/actions/version-bump.md) | Bump versions in package manifests, TOML files, and release metadata. |
| [`./actions/release-prepare`](actions/release-prepare/action.yml) | [`docs/actions/release-prepare.md`](docs/actions/release-prepare.md) | Compute release tag/name and generate release notes from changelog content. |
| [`./actions/changesets-release`](actions/changesets-release/action.yml) | [`docs/actions/changesets-release.md`](docs/actions/changesets-release.md) | Create Changesets version PRs or publish Changesets-managed packages. |
| [`./actions/license-scan`](actions/license-scan/action.yml) | [`docs/actions/license-scan.md`](docs/actions/license-scan.md) | Scan package manifests for license declarations and license file coverage. |
| [`./actions/package-metadata`](actions/package-metadata/action.yml) | [`docs/actions/package-metadata.md`](docs/actions/package-metadata.md) | Validate package manifest names, versions, descriptions, licenses, readmes, and URLs. |
| [`./actions/notice-readme-check`](actions/notice-readme-check/action.yml) | [`docs/actions/notice-readme-check.md`](docs/actions/notice-readme-check.md) | Verify README, NOTICE, LICENSE, and package-name consistency. |
| [`./actions/toml-validate`](actions/toml-validate/action.yml) | [`docs/actions/toml-validate.md`](docs/actions/toml-validate.md) | Validate TOML syntax and required package metadata sections. |
| [`./actions/codeql`](actions/codeql/action.yml) | [`docs/actions/codeql.md`](docs/actions/codeql.md) | Run CodeQL init, optional autobuild, and analyze. |
| [`./actions/dependency-review`](actions/dependency-review/action.yml) | [`docs/actions/dependency-review.md`](docs/actions/dependency-review.md) | Run GitHub dependency review with reusable policy inputs. |
| [`./actions/security-gate`](actions/security-gate/action.yml) | [`docs/actions/security-gate.md`](docs/actions/security-gate.md) | Aggregate license, metadata, TOML, dependency review, and CodeQL checks. |
| [`./actions/artifact-attestation`](actions/artifact-attestation/action.yml) | [`docs/actions/artifact-attestation.md`](docs/actions/artifact-attestation.md) | Generate build provenance attestations for artifact paths. |
| [`./actions/release-attestation`](actions/release-attestation/action.yml) | [`docs/actions/release-attestation.md`](docs/actions/release-attestation.md) | Generate provenance attestations for release asset files. |
| [`./actions/sign-artifacts`](actions/sign-artifacts/action.yml) | [`docs/actions/sign-artifacts.md`](docs/actions/sign-artifacts.md) | Sign files with cosign keyless or key-based signing. |
| [`./actions/verify-attestations`](actions/verify-attestations/action.yml) | [`docs/actions/verify-attestations.md`](docs/actions/verify-attestations.md) | Verify GitHub artifact attestations and optional cosign signatures. |

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
| [`.github/workflows/reusable-node-lint-typecheck.yml`](.github/workflows/reusable-node-lint-typecheck.yml) | [`docs/actions/node-lint-typecheck.md`](docs/actions/node-lint-typecheck.md) | Checkout, Node setup, install, lint, typecheck, test, and build. |
| [`.github/workflows/reusable-node-version-matrix.yml`](.github/workflows/reusable-node-version-matrix.yml) | [`docs/actions/node-lint-typecheck.md`](docs/actions/node-lint-typecheck.md) | Fan out Node checks across Node versions and optional runner sets. |
| [`.github/workflows/reusable-cross-platform-node.yml`](.github/workflows/reusable-cross-platform-node.yml) | [`docs/actions/node-lint-typecheck.md`](docs/actions/node-lint-typecheck.md) | Fan out Node checks across Ubuntu, Windows, and macOS runners. |
| [`.github/workflows/reusable-js-framework-ci.yml`](.github/workflows/reusable-js-framework-ci.yml) | [`docs/actions/js-framework-ci.md`](docs/actions/js-framework-ci.md) | Run framework-aware Vite, Svelte, Vue, React, or generic frontend CI. |
| [`.github/workflows/reusable-js-framework-matrix.yml`](.github/workflows/reusable-js-framework-matrix.yml) | [`docs/actions/js-framework-ci.md`](docs/actions/js-framework-ci.md) | Fan out framework-aware frontend CI across framework cells, Node versions, and runners. |
| [`.github/workflows/reusable-node-framework-version-matrix.yml`](.github/workflows/reusable-node-framework-version-matrix.yml) | [`docs/actions/js-framework-ci.md`](docs/actions/js-framework-ci.md) | Fan out frontend CI across Node versions and framework-specific package directories. |
| [`.github/workflows/reusable-playwright.yml`](.github/workflows/reusable-playwright.yml) | [`docs/actions/playwright-ci.md`](docs/actions/playwright-ci.md) | Run Playwright e2e tests and upload reports, traces, screenshots, and videos. |
| [`.github/workflows/reusable-build-and-commit-dist.yml`](.github/workflows/reusable-build-and-commit-dist.yml) | [`docs/actions/build-and-commit-dist.md`](docs/actions/build-and-commit-dist.md) | Build a frontend distribution directory and commit it back to the branch. |
| [`.github/workflows/reusable-python-uv-ci.yml`](.github/workflows/reusable-python-uv-ci.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Checkout, Python/uv setup, dependency install, optional monorepo `PYTHONPATH`, validation command, and optional artifact upload. |
| [`.github/workflows/reusable-python-version-matrix.yml`](.github/workflows/reusable-python-version-matrix.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Fan out Python/uv checks across Python versions and optional runner sets. |
| [`.github/workflows/reusable-cross-platform-python.yml`](.github/workflows/reusable-cross-platform-python.yml) | [`docs/actions/python-uv.md`](docs/actions/python-uv.md) | Fan out Python/uv checks across Python versions and Ubuntu, Windows, and macOS runners. |
| [`.github/workflows/reusable-tox.yml`](.github/workflows/reusable-tox.yml) | [`docs/actions/tox-ci.md`](docs/actions/tox-ci.md) | Run tox-based Python validation from a reusable workflow wrapper. |
| [`.github/workflows/reusable-tox-matrix.yml`](.github/workflows/reusable-tox-matrix.yml) | [`docs/actions/tox-ci.md`](docs/actions/tox-ci.md) | Fan out tox validation across Python versions, tox environments, and runners. |
| [`.github/workflows/reusable-python-package-matrix-ci.yml`](.github/workflows/reusable-python-package-matrix-ci.yml) | [`docs/actions/python-package-ci.md`](docs/actions/python-package-ci.md) | Fan out package compile, test, docs, build, and artifact checks across Python versions and package cells. |
| [`.github/workflows/reusable-python-package-build.yml`](.github/workflows/reusable-python-package-build.yml) | [`docs/actions/python-package-build.md`](docs/actions/python-package-build.md) | Build one Python package and upload its `dist` output. |
| [`.github/workflows/reusable-rust-ci.yml`](.github/workflows/reusable-rust-ci.yml) | [`docs/actions/rust-cargo-ci.md`](docs/actions/rust-cargo-ci.md) | Checkout, Rust setup, Cargo fmt, clippy, test, build, and optional docs. |
| [`.github/workflows/reusable-rust-version-matrix.yml`](.github/workflows/reusable-rust-version-matrix.yml) | [`docs/actions/rust-cargo-ci.md`](docs/actions/rust-cargo-ci.md) | Fan out Cargo checks across Rust toolchains and optional runner sets. |
| [`.github/workflows/reusable-cross-platform-rust.yml`](.github/workflows/reusable-cross-platform-rust.yml) | [`docs/actions/rust-cargo-ci.md`](docs/actions/rust-cargo-ci.md) | Fan out Cargo checks across Rust toolchains and Ubuntu, Windows, and macOS runners. |
| [`.github/workflows/reusable-os-matrix.yml`](.github/workflows/reusable-os-matrix.yml) | [`docs/actions/os-matrix-cell.md`](docs/actions/os-matrix-cell.md) | Fan out Node, Python, Rust, or generic command checks across Ubuntu, Windows, and macOS runners. |
| [`.github/workflows/reusable-cross-platform-command.yml`](.github/workflows/reusable-cross-platform-command.yml) | [`docs/actions/cross-platform-command.md`](docs/actions/cross-platform-command.md) | Fan out default or OS-specific commands across Ubuntu, Windows, and macOS runners. |
| [`.github/workflows/reusable-build-linux-artifact.yml`](.github/workflows/reusable-build-linux-artifact.yml) | [`docs/actions/platform-artifact-build.md`](docs/actions/platform-artifact-build.md) | Build and upload Linux artifacts. |
| [`.github/workflows/reusable-build-windows-artifact.yml`](.github/workflows/reusable-build-windows-artifact.yml) | [`docs/actions/platform-artifact-build.md`](docs/actions/platform-artifact-build.md) | Build and upload Windows artifacts. |
| [`.github/workflows/reusable-build-darwin-artifact.yml`](.github/workflows/reusable-build-darwin-artifact.yml) | [`docs/actions/platform-artifact-build.md`](docs/actions/platform-artifact-build.md) | Build and upload Darwin/macOS artifacts. |
| [`.github/workflows/reusable-build-android-artifact.yml`](.github/workflows/reusable-build-android-artifact.yml) | [`docs/actions/android-artifact-build.md`](docs/actions/android-artifact-build.md) | Build and upload Android APK/AAB artifacts. |
| [`.github/workflows/reusable-electron-release.yml`](.github/workflows/reusable-electron-release.yml) | [`docs/actions/electron-artifact-build.md`](docs/actions/electron-artifact-build.md) | Build and upload Electron desktop installers. |
| [`.github/workflows/reusable-tauri-release.yml`](.github/workflows/reusable-tauri-release.yml) | [`docs/actions/tauri-artifact-build.md`](docs/actions/tauri-artifact-build.md) | Build and upload Tauri desktop bundles. |
| [`.github/workflows/reusable-deb-package-build.yml`](.github/workflows/reusable-deb-package-build.yml) | [`docs/actions/deb-package-build.md`](docs/actions/deb-package-build.md) | Build and upload Debian packages. |
| [`.github/workflows/reusable-snap-build.yml`](.github/workflows/reusable-snap-build.yml) | [`docs/actions/snap-build.md`](docs/actions/snap-build.md) | Build and upload Snap packages. |
| [`.github/workflows/reusable-apt-publish.yml`](.github/workflows/reusable-apt-publish.yml) | [`docs/actions/apt-publish.md`](docs/actions/apt-publish.md) | Publish Debian packages to an APT repository. |
| [`.github/workflows/reusable-rpm-publish.yml`](.github/workflows/reusable-rpm-publish.yml) | [`docs/actions/rpm-publish.md`](docs/actions/rpm-publish.md) | Publish RPM packages to a YUM/DNF repository. |
| [`.github/workflows/reusable-snap-publish.yml`](.github/workflows/reusable-snap-publish.yml) | [`docs/actions/snap-publish.md`](docs/actions/snap-publish.md) | Publish Snap packages to Snapcraft. |
| [`.github/workflows/reusable-brew-publish.yml`](.github/workflows/reusable-brew-publish.yml) | [`docs/actions/brew-publish.md`](docs/actions/brew-publish.md) | Update Homebrew tap formulae or casks through a pull request. |
| [`.github/workflows/reusable-linux-package-publish.yml`](.github/workflows/reusable-linux-package-publish.yml) | [`docs/actions/linux-package-publish.md`](docs/actions/linux-package-publish.md) | Route package publication across APT, RPM, Snapcraft, and Homebrew lanes. |
| [`.github/workflows/reusable-terraform-plan.yml`](.github/workflows/reusable-terraform-plan.yml) | [`docs/actions/terraform-plan.md`](docs/actions/terraform-plan.md) | Run Terraform init, validate, plan, and upload the plan artifact. |
| [`.github/workflows/reusable-terraform-apply.yml`](.github/workflows/reusable-terraform-apply.yml) | [`docs/actions/terraform-apply.md`](docs/actions/terraform-apply.md) | Run Terraform apply with optional plan artifact download and environment gates. |
| [`.github/workflows/reusable-proxmox-plan.yml`](.github/workflows/reusable-proxmox-plan.yml) | [`docs/actions/proxmox-command.md`](docs/actions/proxmox-command.md) | Run Proxmox plan commands and optionally upload outputs. |
| [`.github/workflows/reusable-proxmox-apply.yml`](.github/workflows/reusable-proxmox-apply.yml) | [`docs/actions/proxmox-command.md`](docs/actions/proxmox-command.md) | Run Proxmox apply commands behind optional environment gates. |
| [`.github/workflows/reusable-docs-build.yml`](.github/workflows/reusable-docs-build.yml) | [`docs/actions/docs-build.md`](docs/actions/docs-build.md) | Build documentation and upload generated site artifacts. |
| [`.github/workflows/reusable-pages-deploy.yml`](.github/workflows/reusable-pages-deploy.yml) | [`docs/actions/pages-deploy.md`](docs/actions/pages-deploy.md) | Upload and deploy GitHub Pages artifacts. |
| [`.github/workflows/reusable-static-app-build.yml`](.github/workflows/reusable-static-app-build.yml) | [`docs/actions/static-app-build.md`](docs/actions/static-app-build.md) | Build static apps and upload generated output. |
| [`.github/workflows/reusable-static-app-deploy.yml`](.github/workflows/reusable-static-app-deploy.yml) | [`docs/actions/static-app-deploy.md`](docs/actions/static-app-deploy.md) | Deploy static apps with caller-owned provider commands. |
| [`.github/workflows/reusable-cloudflare-pages-deploy.yml`](.github/workflows/reusable-cloudflare-pages-deploy.yml) | [`docs/actions/cloudflare-pages-deploy.md`](docs/actions/cloudflare-pages-deploy.md) | Deploy static apps to Cloudflare Pages. |
| [`.github/workflows/reusable-netlify-deploy.yml`](.github/workflows/reusable-netlify-deploy.yml) | [`docs/actions/netlify-deploy.md`](docs/actions/netlify-deploy.md) | Deploy static apps to Netlify. |
| [`.github/workflows/reusable-vercel-deploy.yml`](.github/workflows/reusable-vercel-deploy.yml) | [`docs/actions/vercel-deploy.md`](docs/actions/vercel-deploy.md) | Deploy static apps to Vercel. |
| [`.github/workflows/reusable-docs-release.yml`](.github/workflows/reusable-docs-release.yml) | [`docs/actions/docs-build.md`](docs/actions/docs-build.md) | Build docs, optionally deploy Pages, and optionally attach docs archives to a GitHub Release. |
| [`.github/workflows/reusable-monorepo-discover.yml`](.github/workflows/reusable-monorepo-discover.yml) | [`docs/actions/monorepo-discover.md`](docs/actions/monorepo-discover.md) | Discover package cells from configured monorepo globs. |
| [`.github/workflows/reusable-monorepo-matrix.yml`](.github/workflows/reusable-monorepo-matrix.yml) | [`docs/actions/monorepo-discover.md`](docs/actions/monorepo-discover.md) | Generate changed-package matrix JSON from monorepo globs. |
| [`.github/workflows/reusable-uv-monorepo-ci.yml`](.github/workflows/reusable-uv-monorepo-ci.yml) | [`docs/actions/uv-monorepo-ci.md`](docs/actions/uv-monorepo-ci.md) | Fan out uv package CI across Python versions and package cells. |
| [`.github/workflows/reusable-pnpm-monorepo-ci.yml`](.github/workflows/reusable-pnpm-monorepo-ci.yml) | [`docs/actions/pnpm-monorepo-ci.md`](docs/actions/pnpm-monorepo-ci.md) | Fan out pnpm package CI across Node versions and package cells. |
| [`.github/workflows/reusable-monorepo-package-ci.yml`](.github/workflows/reusable-monorepo-package-ci.yml) | [`docs/actions/monorepo-discover.md`](docs/actions/monorepo-discover.md) | Route mixed uv/pnpm package cells through their ecosystem CI actions. |
| [`.github/workflows/reusable-monorepo-release-train.yml`](.github/workflows/reusable-monorepo-release-train.yml) | [`docs/actions/monorepo-release-train.md`](docs/actions/monorepo-release-train.md) | Execute ordered commands across package cells for release trains. |
| [`.github/workflows/reusable-monorepo-artifact-join.yml`](.github/workflows/reusable-monorepo-artifact-join.yml) | [`docs/actions/monorepo-artifact-join.md`](docs/actions/monorepo-artifact-join.md) | Join matrix artifacts and verify aggregate output. |
| [`.github/workflows/reusable-changed-files.yml`](.github/workflows/reusable-changed-files.yml) | [`docs/actions/changed-files.md`](docs/actions/changed-files.md) | Detect changed files and derive changed package cells. |
| [`.github/workflows/reusable-git-commit-generated.yml`](.github/workflows/reusable-git-commit-generated.yml) | [`docs/actions/git-commit-generated.md`](docs/actions/git-commit-generated.md) | Commit generated outputs without assuming a specific artifact path. |
| [`.github/workflows/reusable-create-pr.yml`](.github/workflows/reusable-create-pr.yml) | [`docs/actions/create-pr.md`](docs/actions/create-pr.md) | Create or update a pull request for generated changes. |
| [`.github/workflows/reusable-sync-docs.yml`](.github/workflows/reusable-sync-docs.yml) | [`docs/actions/sync-docs.md`](docs/actions/sync-docs.md) | Sync generated docs and open a pull request. |
| [`.github/workflows/reusable-workflow-dispatch-batches.yml`](.github/workflows/reusable-workflow-dispatch-batches.yml) | [`docs/actions/workflow-dispatch-batches.md`](docs/actions/workflow-dispatch-batches.md) | Dispatch child workflows from JSON batch definitions. |
| [`.github/workflows/reusable-ssot-validate.yml`](.github/workflows/reusable-ssot-validate.yml) | [`docs/actions/ssot-validate.md`](docs/actions/ssot-validate.md) | Validate SSOT registries and upload validation reports. |
| [`.github/workflows/reusable-ssot-sync-statuses.yml`](.github/workflows/reusable-ssot-sync-statuses.yml) | [`docs/actions/ssot-sync-statuses.md`](docs/actions/ssot-sync-statuses.md) | Synchronize SSOT implementation status from evidence or repo truth. |
| [`.github/workflows/reusable-ssot-boundary-gate.yml`](.github/workflows/reusable-ssot-boundary-gate.yml) | [`docs/actions/ssot-boundary-gate.md`](docs/actions/ssot-boundary-gate.md) | Gate work on SSOT boundary scope and frozen readiness. |
| [`.github/workflows/reusable-ssot-evidence-lane.yml`](.github/workflows/reusable-ssot-evidence-lane.yml) | [`docs/actions/ssot-evidence-lane.md`](docs/actions/ssot-evidence-lane.md) | Run SSOT evidence lanes and upload evidence artifacts. |
| [`.github/workflows/reusable-ssot-certification-matrix.yml`](.github/workflows/reusable-ssot-certification-matrix.yml) | [`docs/actions/ssot-certification-profile.md`](docs/actions/ssot-certification-profile.md) | Run SSOT certification profiles as a matrix. |
| [`.github/workflows/reusable-ssot-release-certify.yml`](.github/workflows/reusable-ssot-release-certify.yml) | [`docs/actions/ssot-release-certify.md`](docs/actions/ssot-release-certify.md) | Certify, promote, or publish SSOT release entities. |
| [`.github/workflows/reusable-docker-compose-service.yml`](.github/workflows/reusable-docker-compose-service.yml) | [`docs/actions/docker-compose-service.md`](docs/actions/docker-compose-service.md) | Restart/rebuild/log a Docker Compose service from a deployment runner. |
| [`.github/workflows/reusable-pypi-publish.yml`](.github/workflows/reusable-pypi-publish.yml) | [`docs/actions/pypi-publish.md`](docs/actions/pypi-publish.md) | Publish Python distributions to PyPI or TestPyPI. |
| [`.github/workflows/reusable-npm-publish.yml`](.github/workflows/reusable-npm-publish.yml) | [`docs/actions/npm-publish.md`](docs/actions/npm-publish.md) | Publish Node packages to npmjs or another npm-compatible registry. |
| [`.github/workflows/reusable-crates-publish.yml`](.github/workflows/reusable-crates-publish.yml) | [`docs/actions/crates-publish.md`](docs/actions/crates-publish.md) | Publish Rust crates with `cargo publish`. |
| [`.github/workflows/reusable-github-release.yml`](.github/workflows/reusable-github-release.yml) | [`docs/actions/github-release.md`](docs/actions/github-release.md) | Create or update GitHub Releases and upload files. |
| [`.github/workflows/reusable-release-assets.yml`](.github/workflows/reusable-release-assets.yml) | [`docs/actions/release-assets.md`](docs/actions/release-assets.md) | Download artifacts, normalize release assets, and generate checksums. |
| [`.github/workflows/reusable-version-bump.yml`](.github/workflows/reusable-version-bump.yml) | [`docs/actions/version-bump.md`](docs/actions/version-bump.md) | Bump versions in package manifests, TOML files, and release metadata. |
| [`.github/workflows/reusable-release-prepare.yml`](.github/workflows/reusable-release-prepare.yml) | [`docs/actions/release-prepare.md`](docs/actions/release-prepare.md) | Compute release tag/name and generate release notes from changelog content. |
| [`.github/workflows/reusable-changesets-release.yml`](.github/workflows/reusable-changesets-release.yml) | [`docs/actions/changesets-release.md`](docs/actions/changesets-release.md) | Create Changesets version PRs or publish Changesets-managed packages. |
| [`.github/workflows/reusable-license-scan.yml`](.github/workflows/reusable-license-scan.yml) | [`docs/actions/license-scan.md`](docs/actions/license-scan.md) | Scan package manifests for license declarations and license file coverage. |
| [`.github/workflows/reusable-package-metadata.yml`](.github/workflows/reusable-package-metadata.yml) | [`docs/actions/package-metadata.md`](docs/actions/package-metadata.md) | Validate package manifest names, versions, descriptions, licenses, readmes, and URLs. |
| [`.github/workflows/reusable-notice-readme-check.yml`](.github/workflows/reusable-notice-readme-check.yml) | [`docs/actions/notice-readme-check.md`](docs/actions/notice-readme-check.md) | Verify README, NOTICE, LICENSE, and package-name consistency. |
| [`.github/workflows/reusable-toml-validate.yml`](.github/workflows/reusable-toml-validate.yml) | [`docs/actions/toml-validate.md`](docs/actions/toml-validate.md) | Validate TOML syntax and required package metadata sections. |
| [`.github/workflows/reusable-codeql.yml`](.github/workflows/reusable-codeql.yml) | [`docs/actions/codeql.md`](docs/actions/codeql.md) | Run CodeQL init, optional autobuild, and analyze. |
| [`.github/workflows/reusable-dependency-review.yml`](.github/workflows/reusable-dependency-review.yml) | [`docs/actions/dependency-review.md`](docs/actions/dependency-review.md) | Run GitHub dependency review with reusable policy inputs. |
| [`.github/workflows/reusable-security-gate.yml`](.github/workflows/reusable-security-gate.yml) | [`docs/actions/security-gate.md`](docs/actions/security-gate.md) | Aggregate license, metadata, TOML, dependency review, and CodeQL checks. |
| [`.github/workflows/reusable-artifact-attestation.yml`](.github/workflows/reusable-artifact-attestation.yml) | [`docs/actions/artifact-attestation.md`](docs/actions/artifact-attestation.md) | Generate build provenance attestations for artifact paths. |
| [`.github/workflows/reusable-release-attestation.yml`](.github/workflows/reusable-release-attestation.yml) | [`docs/actions/release-attestation.md`](docs/actions/release-attestation.md) | Generate provenance attestations for release asset files. |
| [`.github/workflows/reusable-sign-artifacts.yml`](.github/workflows/reusable-sign-artifacts.yml) | [`docs/actions/sign-artifacts.md`](docs/actions/sign-artifacts.md) | Sign files with cosign keyless or key-based signing. |
| [`.github/workflows/reusable-verify-attestations.yml`](.github/workflows/reusable-verify-attestations.yml) | [`docs/actions/verify-attestations.md`](docs/actions/verify-attestations.md) | Verify GitHub artifact attestations and optional cosign signatures. |

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

The reusable set now covers the first package publication lane, release preparation/version bumping, baseline license/notice/readme/metadata validation, CodeQL, dependency review, aggregate security gates, provenance attestation, cosign signing, attestation/signature verification, Rust/Cargo CI, Node/Python/Rust version fan-out, JavaScript framework CI, Playwright/e2e, tox CI, OS fan-out, platform artifact builds, Android artifacts, Electron/Tauri installers, Debian/Snap builds, apt/rpm/snap/brew publication, Terraform, Proxmox, docs build, Pages deploy, static app deployment, uv/pnpm monorepo CI, monorepo matrix discovery, artifact joining, ordered package release trains, changed-file detection, generated commits, PR creation, docs sync, workflow dispatch batches, and SSOT validation/evidence/certification/release gates. See [`docs/missing-reusable-workflow-families.md`](docs/missing-reusable-workflow-families.md).

## Source Analysis

The first reusable set is grounded in the generated inventory under `reports/`:

- [`reports/workflow-inventory.md`](reports/workflow-inventory.md)
- [`reports/final-workflow-component-analysis.md`](reports/final-workflow-component-analysis.md)
- [`reports/workflows/`](reports/workflows/)
- [`reports/scripts/`](reports/scripts/)

The copied historical workflows remain under `.github/workflows/*__<hash>.yml` for reference. New reusable workflows use the `reusable-*.yml` naming convention.
