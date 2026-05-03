# Cross Platform Command

`actions/cross-platform-command` runs one command with optional Linux, macOS, and Windows overrides.

## Purpose

- Normalize shell dispatch across `ubuntu-latest`, `macos-latest`, and `windows-latest`.
- Keep a single default command for common cases.
- Allow OS-specific command overrides when path separators, shell syntax, or tooling differs.

## Dependencies

- Bash on Linux and macOS runners.
- PowerShell on Windows runners.

## Inputs

| Input | Default | Purpose |
| --- | --- | --- |
| `working-directory` | `.` | Directory where commands execute. |
| `command` | empty | Default command for all operating systems. |
| `linux-command` | empty | Linux override. |
| `macos-command` | empty | macOS override. |
| `windows-command` | empty | Windows override. |

## Reusable Workflow

- `.github/workflows/reusable-cross-platform-command.yml`

## Example

```yaml
jobs:
  smoke:
    uses: cobycloud/actions/.github/workflows/reusable-cross-platform-command.yml@main
    with:
      command: npm test --if-present
      windows-command: npm.cmd test --if-present
```
