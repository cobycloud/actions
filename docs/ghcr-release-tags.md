# GHCR release tags

The shared publisher emits the exact Git release version, removing its leading
`v`. PEP 440 alpha, beta and release candidates (`v0.1.0a22`, `v1.2.3b1`,
`v1.2.3rc1`) and SemVer prereleases (`v1.2.3-alpha.1`) receive only their version
tag. Only plain `vMAJOR.MINOR.PATCH` releases receive major, minor and `latest`
aliases. Automatic latest generation in docker/metadata-action is disabled.

The configurable tag regex controls admission, while a separate strict stable
match controls promotion aliases. Container tag validation still applies when a
caller supplies a permissive regex. Signing and provenance remain digest based.

Regression verification: `python -m unittest discover -s tests -p
test_ghcr_release_tags.py -v` passes four tests exercising the workflow's actual
inline Bash validation and metadata settings. CI repeats these checks on Ubuntu.

This prevents the Portwyrm v0.1.0a22 incident, where SemVer parsing rejected the
PEP 440 version and the hyphen-only prerelease check emitted only `latest`.
The existing signed a22 digest and its manually added version tag remain valid.
No existing registry tags or manifests are deleted by this workflow change.
