# Reusable Component Map

This map converts the workflow inventory into reusable external surfaces. It intentionally starts with high-repeat, low-domain-specific components rather than copying repo-specific release gates verbatim.

## Components

### Node Project CI

- Action: `actions/setup-node-project`
- Workflow: `.github/workflows/reusable-node-ci.yml`
- Replaces repeated jobs that run `actions/setup-node`, `npm ci`, `npm run build`, and `npm test`.
- Main inputs: `node-version`, `working-directory`, `install-command`, `build-command`, `test-command`.
- Domain fit: frontend clients, docs apps, Vite/React apps, Node package validation.

### Node Lint Typecheck

- Action: `actions/node-lint-typecheck`
- Workflows: `.github/workflows/reusable-node-lint-typecheck.yml`, `.github/workflows/reusable-node-version-matrix.yml`, `.github/workflows/reusable-cross-platform-node.yml`
- Replaces repeated jobs that fan out Node versions and run lint, typecheck, test, and build gates.
- Main inputs: `node-version`, `node-versions`, `runners`, `working-directory`, `lint-command`, `typecheck-command`, `test-command`, `build-command`.
- Domain fit: npm packages, frontend packages, and Node libraries that need Node 18/20/22 compatibility checks.

### JavaScript Framework CI

- Action: `actions/js-framework-ci`
- Workflows: `.github/workflows/reusable-js-framework-ci.yml`, `.github/workflows/reusable-js-framework-matrix.yml`, `.github/workflows/reusable-node-framework-version-matrix.yml`
- Replaces repeated Svelte/Vue/React/Vite build and validation jobs, including framework-cell and Node-version fan-out.
- Main inputs: `framework`, `framework-cells`, `node-version`, `node-versions`, `runners`, `working-directory`, `install-command`, command overrides, `artifact-path`.
- Domain fit: Vite apps, Svelte apps, Vue apps, React apps, docs clients, and static frontend bundles.

### Playwright CI

- Action: `actions/playwright-ci`
- Workflow: `.github/workflows/reusable-playwright.yml`
- Replaces repeated browser e2e jobs that install Playwright browsers, run tests, and upload report/trace/screenshot/video artifacts.
- Main inputs: `node-version`, `working-directory`, `install-command`, `browser-install-command`, `test-command`, `report-path`, `results-path`.
- Domain fit: frontend clients, docs apps, browser integration tests, and visual/e2e pre-release gates.

### Build and Commit Dist

- Action: `actions/build-and-commit-dist`
- Workflow: `.github/workflows/reusable-build-and-commit-dist.yml`
- Replaces repeated jobs that build `client/dist` or equivalent generated frontend output and push a bot commit.
- Main inputs: `working-directory`, `install-command`, `build-command`, `dist-path`, `commit-message`.
- Required permission: `contents: write`.
- Domain fit: static clients where generated distribution output is committed.

### Python uv CI

- Action: `actions/python-uv`
- Workflows: `.github/workflows/reusable-python-uv-ci.yml`, `.github/workflows/reusable-python-version-matrix.yml`, `.github/workflows/reusable-cross-platform-python.yml`
- Replaces repeated jobs that set up Python, install `uv`, install dependencies, compute workspace `PYTHONPATH`, and run `pytest` or repo-local validation commands, including Python 3.10 through 3.13 fan-out.
- Main inputs: `python-version`, `python-versions`, `runners`, `working-directory`, `install-command`, `run-command`, `compute-monorepo-pythonpath`.
- Domain fit: Python packages, uv workspaces, Swarmauri/Tigrbl package trees, SSOT validation gates.

### tox CI

- Action: `actions/tox-ci`
- Workflows: `.github/workflows/reusable-tox.yml`, `.github/workflows/reusable-tox-matrix.yml`
- Replaces repeated tox jobs for repos that encode environment fan-out in tox configuration.
- Main inputs: `python-version`, `python-versions`, `tox-envs`, `working-directory`, `install-command`, `tox-command`, `tox-command-base`.
- Domain fit: Python libraries that rely on tox, tox-uv, tox-gh-actions, or existing tox environment definitions.

### Python Package Matrix CI

- Action: `actions/python-package-ci`
- Workflow: `.github/workflows/reusable-python-package-matrix-ci.yml`
- Replaces repeated package-matrix jobs that test package directories across Python versions with compile/test/doc/build checks.
- Main inputs: `python-versions`, `package-cells`, `install-command`, `compile-command`, `test-command`, `docs-command`, `build-command`, `compute-monorepo-pythonpath`.
- Domain fit: Python monorepos, uv workspaces, package-set validation, and package-specific compatibility gates.

### Python Package Build

- Action: `actions/python-package-build`
- Workflow: `.github/workflows/reusable-python-package-build.yml`
- Replaces repeated jobs that call `uv build` for one package and upload the resulting distributions.
- Main inputs: `project-path`, `out-dir`, `artifact-name`.
- Domain fit: PyPI package build lanes and release smoke lanes.

### Rust Cargo CI

- Action: `actions/rust-cargo-ci`
- Workflows: `.github/workflows/reusable-rust-ci.yml`, `.github/workflows/reusable-rust-version-matrix.yml`, `.github/workflows/reusable-cross-platform-rust.yml`
- Replaces repeated Rust jobs that install a toolchain and run Cargo fmt, clippy, test, build, docs, and MSRV/stable/beta/nightly fan-out.
- Main inputs: `rust-toolchain`, `rust-toolchains`, `runners`, `components`, `targets`, `working-directory`, `fmt-command`, `clippy-command`, `test-command`, `build-command`.
- Domain fit: Rust crates, cargo workspaces, crates.io preflight checks, and minimum-supported Rust version gates.

### OS Matrix

- Action: `actions/os-matrix-cell`
- Helper action: `actions/cross-platform-command`
- Workflow: `.github/workflows/reusable-os-matrix.yml`
- Related wrappers: `.github/workflows/reusable-cross-platform-node.yml`, `.github/workflows/reusable-cross-platform-python.yml`, `.github/workflows/reusable-cross-platform-rust.yml`, `.github/workflows/reusable-cross-platform-command.yml`
- Replaces repeated Ubuntu, Windows, and macOS fan-out for Node, Python, Rust, or generic command checks.
- Main inputs: `ecosystem`, `runners`, `version`, `working-directory`, `install-command`, `run-command`, `linux-command`, `macos-command`, `windows-command`.
- Domain fit: cross-platform compatibility checks where the caller needs one runtime family or one OS-aware command across `ubuntu-latest`, `windows-latest`, and `macos-latest`.

### Platform Artifact Build

- Action: `actions/platform-artifact-build`
- Workflows: `.github/workflows/reusable-build-linux-artifact.yml`, `.github/workflows/reusable-build-windows-artifact.yml`, `.github/workflows/reusable-build-darwin-artifact.yml`
- Replaces repeated Linux, Windows, and Darwin artifact build jobs with caller-owned setup/build commands and artifact upload.
- Main inputs: `working-directory`, `setup-command`, `build-command`, `linux-build-command`, `macos-build-command`, `windows-build-command`, `artifact-path`, `artifact-name`.
- Domain fit: CLI binaries, desktop archives, native installers, platform-specific release assets, and pre-signing artifacts.

### Android Artifact Build

- Action: `actions/android-artifact-build`
- Workflow: `.github/workflows/reusable-build-android-artifact.yml`
- Replaces repeated Android Gradle build jobs that produce APK or AAB outputs.
- Main inputs: `working-directory`, `java-version`, `setup-command`, `gradle-command`, `artifact-path`, `artifact-name`.
- Domain fit: Android release artifacts, mobile validation lanes, and APK/AAB release assets.

### Electron Artifact Build

- Action: `actions/electron-artifact-build`
- Workflow: `.github/workflows/reusable-electron-release.yml`
- Replaces repeated Electron package and desktop installer jobs.
- Main inputs: `node-version`, `working-directory`, `install-command`, `build-command`, `artifact-path`, `artifact-name`.
- Domain fit: Electron desktop shell packaging and generated desktop installers.

### Tauri Artifact Build

- Action: `actions/tauri-artifact-build`
- Workflow: `.github/workflows/reusable-tauri-release.yml`
- Replaces repeated Tauri package and desktop bundle jobs.
- Main inputs: `node-version`, `rust-toolchain`, `working-directory`, `linux-deps-command`, `install-command`, `build-command`, `artifact-path`.
- Domain fit: Rust-backed desktop apps and cross-platform Tauri bundles.

### Linux Package Manager Publication

- Build actions: `actions/deb-package-build`, `actions/snap-build`
- Publish actions: `actions/apt-publish`, `actions/rpm-publish`, `actions/snap-publish`, `actions/brew-publish`
- Workflows: `.github/workflows/reusable-deb-package-build.yml`, `.github/workflows/reusable-snap-build.yml`, `.github/workflows/reusable-apt-publish.yml`, `.github/workflows/reusable-rpm-publish.yml`, `.github/workflows/reusable-snap-publish.yml`, `.github/workflows/reusable-brew-publish.yml`, `.github/workflows/reusable-linux-package-publish.yml`
- Replaces repeated package build and publication jobs for Debian/APT repositories, RPM/YUM/DNF repositories, Snapcraft, and Homebrew taps.
- Main inputs: `build-command`, `artifact-path`, `package-manager`, `package-path`, `publish-command`, `snap-file`, `release`, `tap-repository`, `update-command`.
- Domain fit: installer distribution channels after artifact build, signing, attestation, and release publication.

### Docker Compose Service

- Action: `actions/docker-compose-service`
- Workflow: `.github/workflows/reusable-docker-compose-service.yml`
- Replaces repeated deployment-runner jobs that stop, remove, prune, rebuild, and restart a single Compose service, or collect service logs.
- Main inputs: `compose-command`, `compose-file`, `service`, `operation`, `prune`, `logs-output`.
- Domain fit: self-hosted deployment runners and app stacks with client/backend/relay/minio service lanes.

### Terraform

- Actions: `actions/terraform-plan`, `actions/terraform-apply`
- Workflows: `.github/workflows/reusable-terraform-plan.yml`, `.github/workflows/reusable-terraform-apply.yml`
- Replaces repeated Terraform jobs that run init, validate, plan, artifact upload, and gated apply.
- Main inputs: `working-directory`, `terraform-version`, `init-command`, `validate-command`, `plan-command`, `apply-command`, `plan-artifact-name`, `environment`.
- Domain fit: infrastructure-as-code plan/apply lanes with caller-owned backend and cloud credentials.

### Proxmox

- Action: `actions/proxmox-command`
- Workflows: `.github/workflows/reusable-proxmox-plan.yml`, `.github/workflows/reusable-proxmox-apply.yml`
- Replaces repeated Proxmox VM setup/management jobs while keeping host credentials and tooling caller-owned.
- Main inputs: `working-directory`, `setup-command`, `plan-command`, `apply-command`, `upload-artifact-path`, `environment`.
- Domain fit: Proxmox VM intent validation, plan/apply operations, and self-hosted infrastructure management.

### Docs and Static Deployment

- Actions: `actions/docs-build`, `actions/pages-deploy`, `actions/static-app-build`, `actions/static-app-deploy`, `actions/cloudflare-pages-deploy`, `actions/netlify-deploy`, `actions/vercel-deploy`
- Workflows: `.github/workflows/reusable-docs-build.yml`, `.github/workflows/reusable-pages-deploy.yml`, `.github/workflows/reusable-static-app-build.yml`, `.github/workflows/reusable-static-app-deploy.yml`, `.github/workflows/reusable-cloudflare-pages-deploy.yml`, `.github/workflows/reusable-netlify-deploy.yml`, `.github/workflows/reusable-vercel-deploy.yml`, `.github/workflows/reusable-docs-release.yml`
- Replaces repeated documentation build, GitHub Pages deploy, provider-neutral static app deploy, Cloudflare Pages, Netlify, Vercel, and docs release attachment jobs.
- Main inputs: `working-directory`, `setup-command`, `build-command`, `output-path`, `path`, `deploy-command`, `project-name`, `site-id`, `production`, `deploy-pages`, `tag-name`.
- Domain fit: MkDocs, Sphinx, VitePress, Docusaurus, generated static docs, GitHub Pages, Cloudflare Pages, Netlify, Vercel, and provider-neutral static deployments.

### Monorepo and Set-Based Execution

- Discovery/action primitives: `actions/monorepo-discover`, `actions/monorepo-artifact-join`, `actions/monorepo-release-train`
- Ecosystem CI actions: `actions/uv-monorepo-ci`, `actions/pnpm-monorepo-ci`
- Workflows: `.github/workflows/reusable-monorepo-discover.yml`, `.github/workflows/reusable-monorepo-matrix.yml`, `.github/workflows/reusable-uv-monorepo-ci.yml`, `.github/workflows/reusable-pnpm-monorepo-ci.yml`, `.github/workflows/reusable-monorepo-package-ci.yml`, `.github/workflows/reusable-monorepo-release-train.yml`, `.github/workflows/reusable-monorepo-artifact-join.yml`
- Replaces repeated package discovery, changed-set matrix generation, uv workspace package validation, pnpm workspace package validation, ordered release trains, and matrix artifact joining.
- Main inputs: `package-globs`, `changed-only`, `base-ref`, `head-ref`, `package-cells`, `python-versions`, `node-versions`, `command`, `artifact-pattern`, `expected-count`.
- Domain fit: uv workspaces, Python package monorepos, pnpm workspaces, app/package sets, package-specific CI, and ordered package publication trains.

### Git and Pull Request Automation

- Actions: `actions/changed-files`, `actions/git-commit-generated`, `actions/create-pr`, `actions/sync-docs`, `actions/workflow-dispatch-batches`
- Workflows: `.github/workflows/reusable-changed-files.yml`, `.github/workflows/reusable-git-commit-generated.yml`, `.github/workflows/reusable-create-pr.yml`, `.github/workflows/reusable-sync-docs.yml`, `.github/workflows/reusable-workflow-dispatch-batches.yml`
- Replaces repeated changed-file detection, generated-output commits, pull request creation, versioned docs sync, and workflow dispatch batch jobs.
- Main inputs: `base-ref`, `head-ref`, `package-globs`, `paths`, `commit-message`, `branch`, `title`, `sync-command`, `batches-json`.
- Domain fit: generated docs/metadata updates, changed package routing, batch orchestration, and pull-request-based automation.

### SSOT Gates and Automation

- Actions: `actions/ssot-validate`, `actions/ssot-sync-statuses`, `actions/ssot-boundary-gate`, `actions/ssot-evidence-lane`, `actions/ssot-certification-profile`, `actions/ssot-release-certify`
- Workflows: `.github/workflows/reusable-ssot-validate.yml`, `.github/workflows/reusable-ssot-sync-statuses.yml`, `.github/workflows/reusable-ssot-boundary-gate.yml`, `.github/workflows/reusable-ssot-evidence-lane.yml`, `.github/workflows/reusable-ssot-certification-matrix.yml`, `.github/workflows/reusable-ssot-release-certify.yml`
- Replaces repeated SSOT validation, status sync, boundary readiness, evidence, certification profile, and release certify/promote/publish gates.
- Main inputs: `registry-path`, `boundary-id`, `release-id`, `profile-ids`, `evidence-id`, `evidence-path`, `fail-closed`, `ssot-command`.
- Domain fit: SSOT-governed repositories that need fail-closed gates while keeping repo-specific registry layout and command variants explicit.

### PyPI Publish

- Actions: `actions/pypi-publish`, `actions/pypi-token-publish`, `actions/pypi-trusted-publish`
- Workflow: `.github/workflows/reusable-pypi-publish.yml`
- Replaces repeated jobs that publish prebuilt Python distributions with `uv publish`.
- Main inputs: `packages-dir`, `repository-url`, `skip-existing`; token-only lanes also require `token`.
- Domain fit: Python package release lanes that must choose API-token-only or Trusted-Publishing-only behavior explicitly.

### npm Publish

- Action: `actions/npm-publish`
- Workflow: `.github/workflows/reusable-npm-publish.yml`
- Replaces repeated jobs that publish Node packages to npmjs or another npm-compatible registry.
- Main inputs: `package-directory`, `registry-url`, `scope`, `tag`, `access`, `provenance`, `dry-run`.
- Domain fit: Node package release lanes, Changesets-backed publish jobs, and npm provenance.

### crates.io Publish

- Action: `actions/crates-publish`
- Workflow: `.github/workflows/reusable-crates-publish.yml`
- Replaces repeated jobs that publish Rust crates with `cargo publish`.
- Main inputs: `rust-toolchain`, `working-directory`, `registry`, `package`, `features`, `dry-run`.
- Domain fit: Rust crate release lanes and publish dry-runs.

### GitHub Release

- Action: `actions/github-release`
- Workflow: `.github/workflows/reusable-github-release.yml`
- Replaces repeated jobs that create GitHub Releases and upload assets.
- Main inputs: `tag-name`, `name`, `body`, `body-path`, `files`, `draft`, `prerelease`, `make-latest`.
- Domain fit: release asset publication and release note publication.

### Release Assets

- Action: `actions/release-assets`
- Workflow: `.github/workflows/reusable-release-assets.yml`
- Replaces repeated jobs that collect build artifacts, flatten release assets, and generate SHA-256 checksums.
- Main inputs: `artifact-name`, `source-path`, `output-path`, `checksum-file`, `normalized-artifact-name`.
- Domain fit: multi-artifact release preparation before GitHub Release upload.

### Version Bump

- Action: `actions/version-bump`
- Workflow: `.github/workflows/reusable-version-bump.yml`
- Replaces repeated version edits across `package.json`, `pyproject.toml`, `Cargo.toml`, and release metadata files.
- Main inputs: `version`, `package-json-files`, `pyproject-files`, `cargo-files`, `extra-version-files`, `update-lockfiles`.
- Domain fit: release preparation before package build/publish lanes.

### Release Prepare

- Action: `actions/release-prepare`
- Workflow: `.github/workflows/reusable-release-prepare.yml`
- Replaces repeated tag-name/release-name computation and changelog-to-release-notes extraction.
- Main inputs: `version`, `tag-prefix`, `release-name`, `changelog-path`, `release-notes-output`, `validate-version-files`.
- Domain fit: release metadata normalization before GitHub Release and registry publication.

### Changesets Release

- Action: `actions/changesets-release`
- Workflow: `.github/workflows/reusable-changesets-release.yml`
- Replaces repeated Changesets version PR and npm publish orchestration.
- Main inputs: `package-directory`, `version-command`, `publish-command`, `commit`, `title`, `create-github-releases`.
- Domain fit: Node monorepos that use Changesets for versioning and changelog generation.

### License Scan

- Action: `actions/license-scan`
- Workflow: `.github/workflows/reusable-license-scan.yml`
- Replaces repeated license declaration and license-file validation jobs.
- Main inputs: `manifest-globs`, `license-file-globs`, `allowed-licenses`, `fail-on-missing`, `fail-on-disallowed`.
- Domain fit: package compliance gates before release.

### Package Metadata

- Action: `actions/package-metadata`
- Workflow: `.github/workflows/reusable-package-metadata.yml`
- Replaces repeated package manifest metadata checks.
- Main inputs: `manifest-globs`, `require-description`, `require-license`, `require-readme`, `require-url`.
- Domain fit: Python, Node, and Rust package metadata validation.

### Notice README Check

- Action: `actions/notice-readme-check`
- Workflow: `.github/workflows/reusable-notice-readme-check.yml`
- Replaces repeated README, NOTICE, LICENSE, and package-name consistency checks.
- Main inputs: `package-roots`, `require-notice`, `require-license`, `require-readme`, `package-name-required-in-readme`.
- Domain fit: package documentation and notice compliance gates.

### TOML Validate

- Action: `actions/toml-validate`
- Workflow: `.github/workflows/reusable-toml-validate.yml`
- Replaces repeated TOML syntax and metadata-section validation.
- Main inputs: `toml-globs`, `require-known-package-section`.
- Domain fit: Python/Rust package manifest validation.

### CodeQL

- Action: `actions/codeql`
- Workflow: `.github/workflows/reusable-codeql.yml`
- Replaces repeated CodeQL init/autobuild/analyze jobs.
- Main inputs: `languages`, `build-mode`, `queries`, `config-file`, `category`, `upload`.
- Domain fit: GitHub code scanning for supported CodeQL languages.

### Dependency Review

- Action: `actions/dependency-review`
- Workflow: `.github/workflows/reusable-dependency-review.yml`
- Replaces repeated pull-request dependency review jobs.
- Main inputs: `fail-on-severity`, `allow-licenses`, `deny-licenses`, `deny-packages`, `config-file`.
- Domain fit: pull-request vulnerability and license review.

### Security Gate

- Action: `actions/security-gate`
- Workflow: `.github/workflows/reusable-security-gate.yml`
- Replaces repeated aggregate security/compliance jobs.
- Main inputs: `run-license-scan`, `run-package-metadata`, `run-toml-validate`, `run-dependency-review`, `run-codeql`, `codeql-languages`.
- Domain fit: single security gate combining local metadata checks, dependency review, and CodeQL.

### Artifact Attestation

- Action: `actions/artifact-attestation`
- Workflow: `.github/workflows/reusable-artifact-attestation.yml`
- Replaces repeated build provenance attestation jobs.
- Main inputs: `subject-path`, `subject-name`, `push-to-registry`, `show-summary`.
- Domain fit: build artifact provenance before release or publication.

### Release Attestation

- Action: `actions/release-attestation`
- Workflow: `.github/workflows/reusable-release-attestation.yml`
- Replaces repeated release asset attestation jobs.
- Main inputs: `release-assets-path`, `subject-name`, `push-to-registry`, `show-summary`.
- Domain fit: release bundle and release asset provenance.

### Sign Artifacts

- Action: `actions/sign-artifacts`
- Workflow: `.github/workflows/reusable-sign-artifacts.yml`
- Replaces repeated cosign signing jobs.
- Main inputs: `artifact-path`, `cosign-version`, `key`, `password`, `recursive`.
- Domain fit: keyless or key-based artifact signing before publication.

### Verify Attestations

- Action: `actions/verify-attestations`
- Workflow: `.github/workflows/reusable-verify-attestations.yml`
- Replaces repeated provenance and signature verification jobs.
- Main inputs: `subject-path`, `owner`, `repo`, `verify-gh-attestations`, `verify-cosign-signatures`, `certificate-identity`.
- Domain fit: release gates that must verify provenance and signature material before publish.

## Deferred Components

These were visible in the inventory but are intentionally deferred until their contracts are normalized:

- SSOT release/certification gates: now covered with explicit registry, boundary, release, profile, and evidence contracts; repo-specific command variants remain caller-owned.
- Tigrbl/tigrbl_auth proof lanes: reusable through the SSOT evidence/certification wrappers when callers provide their evidence commands.
- Multi-package release trains: useful for `ssot-registry` and SDK-style repos, but they need a matrix manifest input rather than hard-coded package lists. The new publish actions are single-package/single-release building blocks, not a train orchestrator.
- Cloud deployment docs lanes: now covered by provider-neutral docs/static wrappers; provider-specific secret names remain caller-owned.
- Visual regression lanes: Playwright/e2e is now covered, but image-diff policy and approval semantics still need a separate contract.

See `docs/missing-reusable-workflow-families.md` for the expanded gap list covering broad monorepo/set-based work, visual regression policy, and git automation.
