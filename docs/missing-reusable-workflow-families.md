# Missing Reusable Workflow Families

This document expands the gap analysis from `reports/final-workflow-component-analysis.md`. The current catalog covers only the first baseline families: Node CI, frontend dist commit, Python/uv CI, Python package build, and Docker Compose service operations.

Everything below is either still missing or has now been partially covered by the publish layer.

## Highest Priority

### Package Publication

Implemented families:

- `reusable-pypi-publish.yml`: publish built Python distributions to PyPI or TestPyPI, with explicit token-only and Trusted-Publishing-only composite actions available for caller workflows.
- `reusable-npm-publish.yml`: publish Node packages to npmjs, including registry URL, access level, provenance, and tag/channel inputs.
- `reusable-crates-publish.yml`: publish Rust crates to crates.io, with dry-run and ordered workspace publish support.
- `reusable-github-release.yml`: create or update GitHub Releases, upload assets, attach checksums, and handle prerelease/draft flags.
- `reusable-release-assets.yml`: download build artifacts, normalize names, generate checksums, and upload release assets.

Still missing:

- ordered multi-crate workspace publication
- ordered multi-package release trains
- cross-registry promotion from staging registries to production registries
- apt, snap, and Homebrew publication

Evidence in report:

- PyPI appears through repeated publication jobs, now covered by `uv publish` based CobyCloud actions.
- npm publish appears through Node publish jobs and `changesets/action`.
- crates.io appears through `cargo` and `dtolnay/rust-toolchain` release jobs.
- GitHub Release appears through `softprops/action-gh-release`.

### Release Preparation and Version Bumps

Implemented families:

- `reusable-version-bump.yml`: bump versions in TOML, package manifests, lockfiles, and release metadata.
- `reusable-release-prepare.yml`: validate release metadata, compute version, tag channel, and changelog snippets.
- `reusable-changesets-release.yml`: normalize Changesets release creation and npm publication.

Still missing:

- deep lockfile validation across all package managers
- ordered multi-package version bump plans
- changelog generation for non-Changesets ecosystems
- release metadata validation against repo-specific SSOT/release registries

Required scope:

- Python `pyproject.toml`
- Rust `Cargo.toml`
- Node `package.json`
- workspace lockfiles
- release metadata files
- README/version references when intentionally governed

### License, Notice, README, and Metadata Validation

Implemented families:

- `reusable-license-scan.yml`: license scanning and report upload.
- `reusable-package-metadata.yml`: validate package names, descriptions, classifiers, URLs, entry points, and bundled files.
- `reusable-notice-readme-check.yml`: verify README, NOTICE, LICENSE, and package metadata consistency.
- `reusable-toml-validate.yml`: validate `pyproject.toml`, `Cargo.toml`, and other TOML metadata.

Still missing:

- classifier-specific policy checks
- generated package file inclusion checks against built artifacts
- SPDX expression parsing beyond exact allowlist matching
- repository-specific notice aggregation and third-party attribution generation

Evidence in report:

- `v0.10.0_license-scan.yml`
- `v0.10.0_package-metadata.yaml`
- compliance, metadata, and security validation components

### Security and Dependency Review

Implemented families:

- `reusable-codeql.yml`: CodeQL init/autobuild/analyze with language matrix inputs.
- `reusable-dependency-review.yml`: dependency review for pull requests.
- `reusable-security-gate.yml`: aggregate CodeQL, dependency review, license scan, and metadata validation.

Still missing:

- CodeQL language fan-out matrix workflow
- non-GitHub dependency scanners
- SBOM generation and vulnerability scanning against generated SBOMs
- organization-specific policy bundles

Evidence in report:

- CodeQL appears through `github/codeql-action/init`, `autobuild`, and `analyze`.
- dependency review appears inside quality workflow families.

### Provenance, Attestation, and Signing

Implemented families:

- `reusable-artifact-attestation.yml`: attest build outputs with `actions/attest-build-provenance`.
- `reusable-release-attestation.yml`: attest release bundles and release assets.
- `reusable-sign-artifacts.yml`: sign artifacts after build, before publication.
- `reusable-verify-attestations.yml`: verify provenance and signature material before release.

Still missing:

- organization-specific signing identity policies
- Sigstore bundle archival and verification reports
- non-cosign signing backends
- package-manager-specific signing for apt, snap, and brew outputs

Evidence in report:

- `actions/attest-build-provenance`
- `actions/attest`
- contract and release-bundle attestation jobs

Signing was not represented deeply enough in the extracted report to derive one repo-specific signing contract, so the implemented signing family uses a provider-neutral cosign surface with keyless and key-based modes.

## Ecosystem CI and Fan-Out

### Rust and Cargo

Implemented families:

- `reusable-rust-ci.yml`: setup Rust toolchain, cache, `cargo fmt`, `cargo clippy`, `cargo test`, and `cargo build`.
- `reusable-rust-version-matrix.yml`: fan out over stable, beta, nightly, and minimum-supported Rust version when specified.

Still missing:

- `reusable-rust-publish-dry-run.yml`: run package dry-runs before crates.io publication.
- workspace-aware ordered cargo package validation before publication.

Evidence in report:

- `cargo`
- `dtolnay/rust-toolchain`
- crate validation and publish jobs

### Node Version and Framework Matrix

Implemented families:

- `reusable-node-version-matrix.yml`: fan out across Node versions.
- `reusable-js-framework-ci.yml`: parameterized Svelte/Vue/React/Vite build/test flow.
- `reusable-js-framework-matrix.yml`: fan out framework-aware frontend CI across framework cells, Node versions, and runners.
- `reusable-node-framework-version-matrix.yml`: fan out Node version checks across framework-specific package directories.
- `reusable-node-lint-typecheck.yml`: lint and typecheck lane.
- `reusable-playwright.yml`: browser install, e2e, trace/screenshot/video artifact upload.

Still missing:

- visual regression policy lanes.

Evidence in report:

- `npm/npx` is the largest atomic command surface.
- Node CI, lint/typecheck, integration, e2e, visual, extension bundle, and frontend publish jobs recur.

### Python Version Matrix

Implemented families:

- `reusable-python-version-matrix.yml`: fan out Python 3.10, 3.11, 3.12, 3.13, and future 3.x versions below Python 4.
- `reusable-tox.yml`: tox-driven matrix lanes for repos that already encode environments in `tox.ini`.
- `reusable-tox-matrix.yml`: fan out tox validation across Python versions, tox environments, and runners.
- `reusable-python-package-matrix-ci.yml`: test package cells across Python versions with compile/test/doc/build checks.

Still missing:

- matrix artifact aggregation for package-specific reports.

Evidence in report:

- `ssot-registry` package CI uses Python 3.10 through 3.13.
- `tox`, `uv`, `python`, and `pip` recur in validation and certification lanes.

### OS Matrix

Implemented families:

- `reusable-os-matrix.yml`: fan out over `ubuntu-latest`, `windows-latest`, and `macos-latest`.
- `reusable-cross-platform-python.yml`: Python/uv checks across OS and Python versions.
- `reusable-cross-platform-node.yml`: Node checks across OS and Node versions.
- `reusable-cross-platform-rust.yml`: Cargo checks across OS and Rust toolchains.
- `actions/os-matrix-cell`: action-level OS cell contract for Node, Python, Rust, and generic commands.
- `actions/cross-platform-command` and `reusable-cross-platform-command.yml`: run default or OS-specific commands across Linux, macOS, and Windows.

The current first-pass reports mostly show Linux/self-hosted runners, but the reusable catalog should support OS fan-out because external consumers need it.

## Artifacts and Installers

### Desktop, Mobile, and OS Artifacts

Implemented families:

- `reusable-build-linux-artifact.yml`
- `reusable-build-windows-artifact.yml`
- `reusable-build-darwin-artifact.yml`
- `reusable-build-android-artifact.yml`
- `reusable-electron-release.yml`
- `reusable-tauri-release.yml`
- `actions/platform-artifact-build`: common platform artifact build/upload cell.
- `actions/android-artifact-build`: Android Java/Gradle APK/AAB build cell.
- `actions/electron-artifact-build`: Electron desktop package cell.
- `actions/tauri-artifact-build`: Tauri Node/Rust desktop bundle cell.

Evidence in report:

- Android jobs use `actions/setup-java` and `reactivecircus/android-emulator-runner`.
- desktop shell, Android APK validation, desktop publish, and release jobs recur in `markdown_workspace`.

### Linux and Package Manager Publication

Implemented families:

- `reusable-deb-package-build.yml`: build Debian packages and upload `.deb` outputs.
- `reusable-snap-build.yml`: build Snap packages and upload `.snap` outputs.
- `reusable-apt-publish.yml`: publish Debian packages to an APT repository.
- `reusable-rpm-publish.yml`: publish RPM packages to a YUM/DNF repository.
- `reusable-snap-publish.yml`: publish Snap packages.
- `reusable-brew-publish.yml`: update Homebrew formulae or taps.
- `reusable-linux-package-publish.yml`: route package publication across APT, RPM, Snapcraft, and Homebrew lanes.
- `actions/deb-package-build`: build and upload `.deb` artifacts.
- `actions/snap-build`: build and upload `.snap` artifacts.
- `actions/apt-publish`: verify Debian packages and run caller-owned APT publish commands.
- `actions/rpm-publish`: verify RPM packages and run caller-owned RPM repository publish commands.
- `actions/snap-publish`: publish `.snap` files with Snapcraft credentials.
- `actions/brew-publish`: update a Homebrew tap through a pull request.

These are not materially represented in the current report, but they are real external release lanes and should be reserved in the roadmap rather than forced into generic release assets.

## Infrastructure and Deployment

### Terraform and Proxmox

Implemented families:

- `reusable-terraform-plan.yml`: setup Terraform, init, validate, plan, and upload plan.
- `reusable-terraform-apply.yml`: apply with environment gates.
- `reusable-proxmox-plan.yml`: validate Proxmox VM intent using Terraform or repo-local tooling.
- `reusable-proxmox-apply.yml`: apply Proxmox VM setup/management operations.
- `actions/terraform-plan`: Terraform init/validate/plan and plan artifact upload.
- `actions/terraform-apply`: Terraform apply with optional plan artifact download.
- `actions/proxmox-command`: caller-owned Proxmox plan/apply command execution and optional artifact upload.

Evidence in report:

- `terraform`
- `hashicorp/setup-terraform`
- `proxmox-vm-setup`
- `promox-vm_management`

### Docs and Static App Deployment

Implemented families:

- `reusable-docs-build.yml`: build documentation with caller-supplied command.
- `reusable-pages-deploy.yml`: upload Pages artifact and deploy GitHub Pages.
- `reusable-static-app-build.yml`: build a static app and upload generated output.
- `reusable-static-app-deploy.yml`: provider-neutral static app deploy wrapper.
- `reusable-cloudflare-pages-deploy.yml`: deploy a static app to Cloudflare Pages.
- `reusable-netlify-deploy.yml`: deploy a static app to Netlify.
- `reusable-vercel-deploy.yml`: deploy a static app to Vercel.
- `reusable-docs-release.yml`: combine docs build, artifact upload, Pages deploy, and release attachment.
- `actions/docs-build`: build docs and upload generated site artifacts.
- `actions/pages-deploy`: configure, upload, and deploy GitHub Pages artifacts.
- `actions/static-app-build`: build a static app and upload generated output.
- `actions/static-app-deploy`: provider-neutral static app build/deploy command execution.
- `actions/cloudflare-pages-deploy`: deploy static apps to Cloudflare Pages.
- `actions/netlify-deploy`: deploy static apps to Netlify.
- `actions/vercel-deploy`: deploy static apps to Vercel.

Evidence in report:

- `actions/upload-pages-artifact`
- `actions/deploy-pages`
- docs deployment workflows for Peagen, Swarmauri SDK, and Tigrcorn

## Git Automation and Monorepo Work

### Git and Pull Request Automation

Implemented families:

- `reusable-changed-files.yml`: detect changed files and expose package/app sets.
- `reusable-create-pr.yml`: create or update a pull request from generated changes.
- `reusable-sync-docs.yml`: sync versioned docs and open a PR.
- `reusable-git-commit-generated.yml`: commit generated outputs without assuming frontend dist.
- `reusable-workflow-dispatch-batches.yml`: dispatch child workflows or batch lanes.
- `actions/changed-files`: changed-file and changed-package-cell JSON output.
- `actions/create-pr`: generated-change pull request creation.
- `actions/sync-docs`: docs sync command plus pull request creation.
- `actions/git-commit-generated`: generic generated-output commit.
- `actions/workflow-dispatch-batches`: JSON-driven child workflow dispatch.

Evidence in report:

- changed-file detection
- `peter-evans/create-pull-request`
- `actions/github-script`
- dispatch-batches
- sync-versioned-docs

### Monorepo and Set-Based Execution

Implemented families:

- `reusable-monorepo-discover.yml`: discover packages/apps from configured globs.
- `reusable-monorepo-matrix.yml`: generate matrix JSON from changed package sets.
- `reusable-monorepo-package-ci.yml`: run package CI over a matrix of package metadata.
- `reusable-monorepo-release-train.yml`: build, validate, and publish ordered package sets.
- `reusable-monorepo-artifact-join.yml`: collect artifacts from matrix jobs and verify the full set.
- `reusable-uv-monorepo-ci.yml`: fan out uv-based package CI across Python versions and package cells.
- `reusable-pnpm-monorepo-ci.yml`: fan out pnpm-based package CI across Node versions and package cells.
- `actions/monorepo-discover`: package cell discovery from globs and optional changed-file filtering.
- `actions/uv-monorepo-ci`: one uv/Python package CI cell.
- `actions/pnpm-monorepo-ci`: one pnpm/Node package CI cell.
- `actions/monorepo-release-train`: ordered command execution across package cells.
- `actions/monorepo-artifact-join`: collect and verify matrix artifacts.

Evidence in report:

- `generate-chunks`
- `set-matrix`
- `dispatch-batches`
- `ssot-registry` package matrix
- Swarmauri SDK mono prepare/validate/publish batch workflows

## SSOT Gates and Automation

Implemented families:

- `reusable-ssot-validate.yml`: run SSOT validation and upload reports.
- `reusable-ssot-sync-statuses.yml`: synchronize implementation status from evidence when supported by the target repo.
- `reusable-ssot-boundary-gate.yml`: validate frozen/current boundary scope.
- `reusable-ssot-evidence-lane.yml`: run evidence lanes and upload evidence artifacts.
- `reusable-ssot-certification-matrix.yml`: execute certification profiles and collect matrix evidence.
- `reusable-ssot-release-certify.yml`: certify/promote/publish SSOT release entities.
- `actions/ssot-validate`: validation with explicit registry and optional report path.
- `actions/ssot-sync-statuses`: status sync with evidence path and fail-on-changes control.
- `actions/ssot-boundary-gate`: boundary readiness gate with boundary ID and fail-closed control.
- `actions/ssot-evidence-lane`: evidence command execution with registry, boundary, profile, evidence ID, and evidence path inputs.
- `actions/ssot-certification-profile`: one certification profile cell with profile ID and optional boundary ID.
- `actions/ssot-release-certify`: release certify/promote/publish operation with release ID.

Evidence in report:

- Tigrbl evidence lanes and gates
- tigrbl_auth certification matrix, contracts, quality, evidence, release bundle
- ssot-registry package CI and release train

These are implemented as SSOT-specific contracts with explicit inputs for registry path, boundary/release IDs, profile selectors, evidence output path, and fail-closed behavior. Repo-specific command variants remain available through override inputs.

## Current Coverage Versus Missing Coverage

| Area | Current Reusable Coverage | Missing Reusable Coverage |
| --- | --- | --- |
| Node CI | Basic install/build/test, version fan-out, framework presets, lint/typecheck, Playwright/e2e artifacts | visual regression policy and browser-project matrix |
| Python CI | Basic uv install/run, Python version matrix, tox matrix, package matrix | release train and aggregate package-report join |
| Rust | Cargo CI, Rust version matrix, crates publish | ordered workspace dry-run and publish trains |
| Docker Compose | service restart/rebuild/logs | deployment promotion gates, service health checks |
| Releases | Python package build only | PyPI, npmjs, crates, GitHub Release, assets, checksums |
| Compliance | none | license scan, notices, README/package metadata, TOML validation |
| Security | CodeQL, dependency review, security aggregate gate | language fan-out, SBOM, external scanners |
| Provenance | attest, sign, verify attestations | organization policy bundles, package-manager signing |
| Docs | docs build, Pages deploy, static app deploy, docs release | provider-specific deploy policy bundles |
| Infra | Terraform plan/apply, Proxmox plan/apply | provider-specific policy bundles |
| Monorepo | changed-set discovery, matrix generation, uv and pnpm package CI, artifact joining, ordered package release trains, git automation integration | provider-specific policy bundles |
| SSOT | validation, status sync, boundary gates, evidence lanes, certification matrix, release certify/promote/publish | provider-specific policy bundles |
| Platform artifacts | Linux, Windows, Darwin, Android, Electron, Tauri, apt, snap, brew | platform-specific signing policy bundles |

## Recommended Build Order

1. Package publication: PyPI, npmjs, crates, GitHub Release.
2. Compliance/security: license scan, metadata/README/TOML checks, dependency review, CodeQL.
3. Matrix CI: Python, Node, Rust, OS fan-out.
4. Docs and Git automation: Pages deploy, changed files, generated commits, PR creation.
5. Provenance/signing: attest, sign, verify.
6. Monorepo release train: discover, matrix, artifact join, ordered publish.
7. SSOT gates: validate, evidence, certification, release closure.
8. Infrastructure and platform artifacts: Terraform, Proxmox, Android, Windows/Darwin/Linux, apt, snap, brew.
