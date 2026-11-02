# Wyrmctl actions

The `wyrmctl-setup`, `wyrmctl-plan`, and `wyrmctl-apply` composite actions provide the
shared Portwyrm control-plane lifecycle. Consumers pin these actions to an immutable
commit, create a plan artifact in a read-only job, and apply that exact artifact only
after the protected environment gate.

The actions accept credentials as inputs but never persist them. Wyrmctl retains its
upstream `NPM_BASE_URL`, `NPM_IDENTITY`, and `NPM_SECRET` environment contract while
talking to the Portwyrm-compatible API.

`wyrmctl-setup` defaults to Wyrmctl `0.4.7`. Consumers may override the exact version,
but deployment workflows should pin this repository to a reviewed immutable commit.

The reusable VM104 Compose workflow invokes `wyrmctl-tls-coverage` before both
planning and applying. Every proxy hostname must be covered by the certificate
referenced by that proxy, and the declared `public-host` must be one of those
proxy hostnames. Exact names and single-label DNS wildcards are supported. The
post-deploy check uses strict HTTPS validation and confirms that the certificate
served for the requested SNI hostname contains that hostname in its SANs.

The reusable workflow checks out this repository's local composite actions at a
reviewed, full-length `cobycloud/actions` commit. It must not use
`github.workflow_sha` for that checkout: in a called workflow GitHub resolves
that value to the caller repository's commit, which is not a valid object in
`cobycloud/actions`.

`wyrmctl-plan` preserves Wyrmctl's safety boundary while supporting reviewed
owned updates. Exit code `1` is accepted only when a non-empty plan artifact was
written, strict artifact inspection succeeds, and both NPM and DNS conflict
collections are empty. Unmanaged, foreign-owned, capability, DNS, malformed,
and missing-artifact plans remain blocking failures.
