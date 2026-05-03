# Release Assets

Composite action: `cobycloud/actions/actions/release-assets@main`

Downloads workflow artifacts, flattens them into a release asset directory, generates SHA-256 checksums, and optionally uploads the normalized asset set.

## Use When

- Build jobs produce artifacts that need consistent release asset names.
- A release job needs a `SHA256SUMS` file.
- Assets from multiple jobs should be flattened before GitHub Release upload.

## Example

```yaml
steps:
  - uses: cobycloud/actions/actions/release-assets@main
    with:
      source-path: release-assets
      output-path: release-assets-normalized
      checksum-file: SHA256SUMS
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `artifact-name` | empty | Optional artifact name. Empty downloads all artifacts. |
| `source-path` | `release-assets` | Artifact download/source path. |
| `output-path` | `release-assets-normalized` | Normalized output path. |
| `checksum-file` | `SHA256SUMS` | Checksum file name. |
| `upload-artifact` | `true` | Upload normalized assets as a workflow artifact. |
| `normalized-artifact-name` | `release-assets` | Artifact name for normalized assets. |

## Outputs

| Output | Description |
| --- | --- |
| `output-path` | Directory containing normalized release assets. |
| `checksum-file` | Checksum file path. |

## Dependencies

- `actions/download-artifact@v4`
- `actions/upload-artifact@v4`
- Bash shell
- `sha256sum`

## Related Reusable Workflow

Use `.github/workflows/reusable-release-assets.yml` for the full reusable job wrapper.
