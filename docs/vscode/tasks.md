# VS Code Tasks

This document owns the finite commands exposed through `.vscode/tasks.json`.
Debugger-oriented and long-running processes are documented separately in
`docs/vscode/launch.md`.

## Task Ownership

Tasks cover:

- Django checks, tests, migrations, translations, and static collection
- Ruff, mypy, YAML, Markdown-link, and dependency-security checks
- runtime and development dependency installation, compilation, synchronization,
  and explicit upgrades
- Docker Compose validation, lifecycle, status, and logs

Tasks intentionally do not appear in **Run and Debug**. Run them through either:

- **Terminal > Run Task...**
- **Ctrl+Shift+P > Tasks: Run Task**

No extension or additional setting is required. If a newly created task file
does not appear immediately, use **Developer: Reload Window** once.

## Environment Files

Tasks do not provide a portable environment-file option equivalent to the
debugger's `envFile`. Django tasks therefore call
`core/development/commands/environment_file_command_runner.py`, which loads
the selected `NAME=VALUE` file before starting `manage.py`. The default input
is `.env`, and another local environment file can be selected when the task
starts.

The parser contract is documented with the owning module in
`docs/core/development/commands/commands.md`.

The runner supports:

- empty lines and full-line comments
- `NAME=VALUE`
- optional `export NAME=VALUE`
- matching single or double quotes around the complete value

It does not interpolate shell variables or execute shell expressions.

## Quality Tasks

The non-mutating `Quality: Run Local Gates` task runs:

1. Django system checks
2. Ruff lint checks
3. Ruff formatting checks
4. the supported incremental mypy scope
5. YAML validation
6. local Markdown-link validation
7. the runtime dependency audit

Tests remain separate because the complete suite requires PostgreSQL and is
longer-running. Migration and translation commands also remain explicit because
they may generate or update tracked files.

`Quality: Ruff Format` changes Python formatting. `Quality: Ruff Fix` applies
safe lint and import fixes. Numbered Django migration files remain excluded by
the shared Ruff configuration.

## Dependency Tasks

Direct runtime dependencies live in `requirements.in`. Direct development
dependencies live in `requirements-dev.in`. Their generated transitive locks
are `requirements.txt` and `requirements-dev.txt`.

Normal operations:

- `Dependencies: Install Runtime Lock` installs the runtime lock
- `Dependencies: Install Runtime And Development Locks` installs both locks
- `Dependencies: Compile Runtime Lock` regenerates the runtime lock without
  requesting upgrades
- `Dependencies: Compile Development Lock` regenerates the development lock
  without requesting upgrades
- `Dependencies: Sync Exact Environment` removes packages outside both locks
  and synchronizes the selected interpreter exactly

Upgrade operations are deliberately separate:

- `Dependencies: Upgrade Runtime Lock`
- `Dependencies: Upgrade Development Lock`

Review generated lock changes and run the complete CI suite after an upgrade.

## Docker Compose Tasks

Every Compose task requests:

- a Compose project name, defaulting to `django-base`
- an environment file, defaulting to `.env`

The project name scopes generated containers, networks, and named volumes. Use
different names for simultaneous clones or local instances.

Project names alone do not isolate host ports. Each simultaneous instance also
needs a different environment file with distinct values for:

- `POSTGRES_PORT`
- `MINIO_API_PORT`
- `MINIO_CONSOLE_PORT`
- `MAILHOG_SMTP_PORT`
- `MAILHOG_UI_PORT`
- `REDIS_PORT`

`Docker: Stop Infrastructure` keeps containers and data.
`Docker: Down (Keep Volumes)` removes containers and networks while preserving
named volumes.

`Docker: DESTRUCTIVE Down And Delete Volumes` passes `--volumes` and deletes
named volumes belonging to the selected Compose project. It does not delete the
independent `minio-data/` bind-mounted directory.

Always verify the selected project name before running the destructive task.
