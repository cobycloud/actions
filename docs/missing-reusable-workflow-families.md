# Missing Reusable Workflow Families

This document expands the gap analysis from `reports/final-workflow-component-analysis.md`. The current catalog covers only the first baseline families: Node CI, frontend dist commit, Python/uv CI, Python package build, and Docker Compose service operations.

Everything below is still missing as a first-class reusable action or reusable workflow family.

## Highest Priority

### Package Publication

Missing families:

- `reusable-pypi-publish.yml`: publish built Python distributions to PyPI or TestPyPI with trusted publishing or token fallback.
- `reusable-npm-publish.yml`: publish Node packages to npmjs, including registry URL, access level, provenance, and tag/channel inputs.
- `reusable-crates-publish.yml`: publish Rust crates to crates.io, with dry-run and ordered workspace publish support.
- `reusable-github-release.yml`: create or update GitHub Releases, upload assets, attach checksums, and handle prerelease/draft flags.
- `reusable-release-assets.yml`: download build artifacts, normalize names, generate checksums, and upload release assets.

Evidence in report:

- PyPI appears through `pypa/gh-action-pypi-publish`.
- npm publish appears through Node publish jobs and `changesets/action`.
- crates.io appears through `cargo` and `dtolnay/rust-toolchain` release jobs.
- GitHub Release appears through `softprops/action-gh-release`.

### Release Preparation and Version Bumps

Missing families:

- `reusable-version-bump.yml`: bump versions in TOML, package manifests, lockfiles, and release metadata.
- `reusable-release-prepare.yml`: validate release metadata, compute version, tag channel, and changelog snippets.
- `reusable-changesets-release.yml`: normalize Changesets release creation and npm publication.

Required scope:

- Python `pyproject.toml`
- Rust `Cargo.toml`
- Node `package.json`
- workspace lockfiles
- release metadata files
- README/version references when intentionally governed

### License, Notice, README, and Metadata Validation

Missing families:

- `reusable-license-scan.yml`: license scanning and report upload.
- `reusable-package-metadata.yml`: validate package names, descriptions, classifiers, URLs, entry points, and bundled files.
- `reusable-notice-readme-check.yml`: verify README, NOTICE, LICENSE, and package metadata consistency.
- `reusable-toml-validate.yml`: validate `pyproject.toml`, `Cargo.toml`, and other TOML metadata.

Evidence in report:

- `v0.10.0_license-scan.yml`
- `v0.10.0_package-metadata.yaml`
- compliance, metadata, and security validation components

### Security and Dependency Review

Missing families:

- `reusable-codeql.yml`: CodeQL init/autobuild/analyze with language matrix inputs.
- `reusable-dependency-review.yml`: dependency review for pull requests.
- `reusable-security-gate.yml`: aggregate CodeQL, dependency review, license scan, and metadata validation.

Evidence in report:

- CodeQL appears through `github/codeql-action/init`, `autobuild`, and `analyze`.
- dependency review appears inside quality workflow families.

### Provenance, Attestation, and Signing

Missing families:

- `reusable-artifact-attestation.yml`: attest build outputs with `actions/attest-build-provenance`.
- `reusable-release-attestation.yml`: attest release bundles and release assets.
- `reusable-sign-artifacts.yml`: sign artifacts after build, before publication.
- `reusable-verify-attestations.yml`: verify provenance and signature material before release.

Evidence in report:

- `actions/attest-build-provenance`
- `actions/attest`
- contract and release-bundle attestation jobs

Signing is not represented deeply enough in the current extracted report to define one signing contract. It should still be a first-class family because it belongs next to provenance and release publication.

## Ecosystem CI and Fan-Out

### Rust and Cargo

Missing families:

- `reusable-rust-ci.yml`: setup Rust toolchain, cache, `cargo fmt`, `cargo clippy`, `cargo test`, and `cargo build`.
- `reusable-rust-publish-dry-run.yml`: run package dry-runs before crates.io publication.
- `reusable-rust-version-matrix.yml`: fan out over stable, beta, nightly, and minimum-supported Rust version when specified.

Evidence in report:

- `cargo`
- `dtolnay/rust-toolchain`
- crate validation and publish jobs

### Node Version and Framework Matrix

Missing families:

- `reusable-node-version-matrix.yml`: fan out across Node versions.
- `reusable-js-framework-ci.yml`: parameterized Svelte/Vue/React/Vite build/test flow.
- `reusable-playwright.yml`: browser install, e2e, trace/screenshot/video artifact upload.
- `reusable-node-lint-typecheck.yml`: lint and typecheck lane.

Evidence in report:

- `npm/npx` is the largest atomic command surface.
- Node CI, lint/typecheck, integration, e2e, visual, extension bundle, and frontend publish jobs recur.

### Python Version Matrix

Missing families:

- `reusable-python-version-matrix.yml`: fan out Python 3.10, 3.11, 3.12, 3.13, and future 3.x versions below Python 4.
- `reusable-python-package-matrix-ci.yml`: test one package across Python versions with compile/test/doc checks.
- `reusable-tox.yml`: tox-driven matrix lanes for repos that already encode environments in `tox.ini`.

Evidence in report:

- `ssot-registry` package CI uses Python 3.10 through 3.13.
- `tox`, `uv`, `python`, and `pip` recur in validation and certification lanes.

### OS Matrix

Missing families:

- `reusable-os-matrix.yml`: fan out over `ubuntu-latest`, `windows-latest`, and `macos-latest`.
- `reusable-cross-platform-python.yml`: Python/uv checks across OS and Python versions.
- `reusable-cross-platform-node.yml`: Node checks across OS and Node versions.
- `reusable-cross-platform-rust.yml`: Cargo checks across OS and Rust toolchains.

The current first-pass reports mostly show Linux/self-hosted runners, but the reusable catalog should support OS fan-out because external consumers need it.

## Artifacts and Installers

### Desktop, Mobile, and OS Artifacts

Missing families:

- `reusable-build-linux-artifact.yml`
- `reusable-build-windows-artifact.yml`
- `reusable-build-darwin-artifact.yml`
- `reusable-build-android-artifact.yml`
- `reusable-electron-release.yml`
- `reusable-tauri-release.yml`

Evidence in report:

- Android jobs use `actions/setup-java` and `reactivecircus/android-emulator-runner`.
- desktop shell, Android APK validation, desktop publish, and release jobs recur in `markdown_workspace`.

### Linux and Package Manager Publication

Missing families:

- `reusable-apt-publish.yml`: publish Debian packages to an APT repository.
- `reusable-snap-publish.yml`: publish Snap packages.
- `reusable-brew-publish.yml`: update Homebrew formulae or taps.

These are not materially represented in the current report, but they are real external release lanes and should be reserved in the roadmap rather than forced into generic release assets.

## Infrastructure and Deployment

### Terraform and Proxmox

Missing families:

- `reusable-terraform-plan.yml`: setup Terraform, init, validate, plan, and upload plan.
- `reusable-terraform-apply.yml`: apply with environment gates.
- `reusable-proxmox-plan.yml`: validate Proxmox VM intent using Terraform or repo-local tooling.
- `reusable-proxmox-apply.yml`: apply Proxmox VM setup/management operations.

Evidence in report:

- `terraform`
- `hashicorp/setup-terraform`
- `proxmox-vm-setup`
- `promox-vm_management`

### Docs and Static App Deployment

Missing families:

- `reusable-docs-build.yml`: build documentation with caller-supplied command.
- `reusable-pages-deploy.yml`: upload Pages artifact and deploy GitHub Pages.
- `reusable-static-app-deploy.yml`: provider-neutral static app deploy wrapper.
- `reusable-docs-release.yml`: combine docs build, artifact upload, Pages deploy, and release attachment.

Evidence in report:

- `actions/upload-pages-artifact`
- `actions/deploy-pages`
- docs deployment workflows for Peagen, Swarmauri SDK, and Tigrcorn

## Git Automation and Monorepo Work

### Git and Pull Request Automation

Missing families:

- `reusable-changed-files.yml`: detect changed files and expose package/app sets.
- `reusable-create-pr.yml`: create or update a pull request from generated changes.
- `reusable-sync-docs.yml`: sync versioned docs and open a PR.
- `reusable-git-commit-generated.yml`: commit generated outputs without assuming frontend dist.
- `reusable-workflow-dispatch-batches.yml`: dispatch child workflows or batch lanes.

Evidence in report:

- changed-file detection
- `peter-evans/create-pull-request`
- `actions/github-script`
- dispatch-batches
- sync-versioned-docs

### Monorepo and Set-Based Execution

Missing families:

- `reusable-monorepo-discover.yml`: discover packages/apps from configured globs.
- `reusable-monorepo-matrix.yml`: generate matrix JSON from changed package sets.
- `reusable-monorepo-package-ci.yml`: run package CI over a matrix of package metadata.
- `reusable-monorepo-release-train.yml`: build, validate, and publish ordered package sets.
- `reusable-monorepo-artifact-join.yml`: collect artifacts from matrix jobs and verify the full set.

Evidence in report:

- `generate-chunks`
- `set-matrix`
- `dispatch-batches`
- `ssot-registry` package matrix
- Swarmauri SDK mono prepare/validate/publish batch workflows

## SSOT Gates and Automation

Missing families:

- `reusable-ssot-validate.yml`: run SSOT validation and upload reports.
- `reusable-ssot-sync-statuses.yml`: synchronize implementation status from evidence when supported by the target repo.
- `reusable-ssot-boundary-gate.yml`: validate frozen/current boundary scope.
- `reusable-ssot-evidence-lane.yml`: run evidence lanes and upload evidence artifacts.
- `reusable-ssot-certification-matrix.yml`: execute certification profiles and collect matrix evidence.
- `reusable-ssot-release-certify.yml`: certify/promote/publish SSOT release entities.

Evidence in report:

- Tigrbl evidence lanes and gates
- tigrbl_auth certification matrix, contracts, quality, evidence, release bundle
- ssot-registry package CI and release train

These should not be generic shell wrappers. They need explicit inputs for registry path, boundary/release IDs, profile selectors, evidence output path, and fail-closed behavior.

## Current Coverage Versus Missing Coverage

| Area | Current Reusable Coverage | Missing Reusable Coverage |
| --- | --- | --- |
| Node CI | Basic install/build/test | version fan-out, framework presets, lint/typecheck, Playwright/e2e/visual |
| Python CI | Basic uv install/run | Python version matrix, tox matrix, package matrix, release train |
| Rust | none | cargo CI, Rust version matrix, crates publish |
| Docker Compose | service restart/rebuild/logs | deployment promotion gates, service health checks |
| Releases | Python package build only | PyPI, npmjs, crates, GitHub Release, assets, checksums |
| Compliance | none | license scan, notices, README/package metadata, TOML validation |
| Security | none | CodeQL, dependency review, security aggregate gate |
| Provenance | none | attest, sign, verify attestations |
| Docs | none | docs build, Pages deploy, static app deploy |
| Infra | none | Terraform, Proxmox |
| Monorepo | none | changed-set discovery, matrix generation, package set release trains |
| SSOT | none | validation, evidence, certification, release gates |
| Platform artifacts | none | Windows, Darwin, Linux, Android, apt, snap, brew |

## Recommended Build Order

1. Package publication: PyPI, npmjs, crates, GitHub Release.
2. Compliance/security: license scan, metadata/README/TOML checks, dependency review, CodeQL.
3. Matrix CI: Python, Node, Rust, OS fan-out.
4. Docs and Git automation: Pages deploy, changed files, generated commits, PR creation.
5. Provenance/signing: attest, sign, verify.
6. Monorepo release train: discover, matrix, artifact join, ordered publish.
7. SSOT gates: validate, evidence, certification, release closure.
8. Infrastructure and platform artifacts: Terraform, Proxmox, Android, Windows/Darwin/Linux, apt, snap, brew.
