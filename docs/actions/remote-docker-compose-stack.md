# Remote Docker Compose Stack

`actions/remote-docker-compose-stack` transfers immutable release directories and operates a
stable Docker Compose project over SSH. The caller owns SSH agent setup, a pinned `known_hosts`
entry, protected-environment approval, secret material, and application health verification.

The remote identity must be able to create `remote-directory` and run `sudo docker compose`
non-interactively. Do not pass private keys or environment values as action inputs. Place runtime
secrets in an existing mode-`0600` remote environment file and provide only its path.

Supported operations are `config`, `deploy`, `start`, `stop`, `restart`, `status`, `logs`, and
`rollback`. Deployments are retained under `remote-directory/releases/<release-id>` and the active
release is recorded by the `current` symlink and `current-release` file.
