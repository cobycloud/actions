# Wyrmctl actions

The `wyrmctl-setup`, `wyrmctl-plan`, and `wyrmctl-apply` composite actions provide the
shared Portwyrm control-plane lifecycle. Consumers pin these actions to an immutable
commit, create a plan artifact in a read-only job, and apply that exact artifact only
after the protected environment gate.

The actions accept credentials as inputs but never persist them. Wyrmctl retains its
upstream `NPM_BASE_URL`, `NPM_IDENTITY`, and `NPM_SECRET` environment contract while
talking to the Portwyrm-compatible API.

`wyrmctl-setup` defaults to Wyrmctl `0.4.5`. Consumers may override the exact version,
but deployment workflows should pin this repository to a reviewed immutable commit.
