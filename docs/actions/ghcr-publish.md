# GHCR Publish

Reusable workflow: `cobycloud/actions/.github/workflows/reusable-ghcr-publish.yml@master`

Publishes a release-tagged, multi-platform OCI image to GHCR with normalized SemVer aliases, BuildKit SBOM and maximal provenance, keyless Cosign signing, GitHub artifact attestation, anonymous pull verification, signature verification, and provenance verification.

## Caller contract

The caller must run its repository-specific tests and vulnerability gates before invoking this workflow. Invoke it only from a protected `vMAJOR.MINOR.PATCH` or prerelease tag.

```yaml
permissions:
  contents: read

jobs:
  gates:
    # Repository-specific tests and vulnerability scans.
    runs-on: ubuntu-latest
    steps:
      - run: echo validate

  publish:
    needs: gates
    permissions:
      contents: read
      packages: write
      id-token: write
      attestations: write
      artifact-metadata: write
    uses: cobycloud/actions/.github/workflows/reusable-ghcr-publish.yml@master
    with:
      image: ghcr.io/example/example
      package-api-path: /orgs/example/packages/container/example
      certificate-identity-regexp: ^https://github.com/example/example/.github/workflows/container.yml@refs/tags/v.*$
      build-args: |
        OCI_REVISION=${{ github.sha }}
        OCI_VERSION=${{ github.ref_name }}
        OCI_SOURCE=https://github.com/${{ github.repository }}
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `image` | required | Fully qualified GHCR image name. |
| `certificate-identity-regexp` | required | Expected keyless-signing identity for the caller workflow. |
| `runner` | `ubuntu-latest` | GitHub runner label. |
| `context` | `.` | Docker build context. |
| `dockerfile` | `Dockerfile` | Dockerfile path. |
| `platforms` | `linux/amd64,linux/arm64` | Target platform list. |
| `build-args` | empty | Newline-separated build arguments. |
| `tag-regex` | strict SemVer release tag | Allowed release-tag expression. |
| `package-api-path` | empty | Optional GitHub API path for package access preflight. |

The workflow intentionally contains no package deletion or pruning behavior.
