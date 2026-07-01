# Continuous Integration Workflow

This document explains the project quality workflow in
`.github/workflows/ci.yaml`.

See also:

- `docs/project.md`
- `docs/github/workflows/discord.md`
- `docs/core/config/config.md`
- `docs/core/config/storage/testing.md`

## Goal

The workflow validates the default Django runtime on every supported push and
pull request without requiring optional external services.

It is project-owned and replaces the need to commit GitHub's generic generated
Django workflow.

## Triggers

Continuous integration runs:

- on pushes to `master`, `develop`, and the established working branch
  patterns
- on pull requests targeting `master` or `develop`
- manually through `workflow_dispatch`

Superseded runs for the same workflow and ref are cancelled.

The workflow uses read-only repository-content permission.

## Supported Runtime

The first CI contract uses:

- Ubuntu's current GitHub-hosted runner
- Python 3.11
- PostgreSQL 16
- dependencies from the pinned `requirements.txt` lock
- GNU gettext for the tracked Spanish catalog

Python 3.11 is the documented minimum and the version used to generate the
current dependency lock. A broader compatibility matrix should be introduced
only when each additional Python version becomes an explicit maintenance
commitment.

## Database Contract

The `django` job starts an isolated PostgreSQL service with neutral CI-only
credentials.

Before Django validation, it:

- waits for PostgreSQL's health check
- creates the `app` schema
- aligns the role search path with the local development contract

No repository or deployment secrets are required.

## Django Gates

The job runs:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test accounts.tests core.tests tenancy.tests
```

Explicit test labels avoid accidental discovery outside the three tracked
project test packages.

Migration drift detection is read-only: it fails when model state would require
an untracked migration, but it does not create a migration file.

The job compiles the tracked Spanish catalog before running tests so
translation assertions execute against the same runtime artifacts expected in
a real installation. Strict catalog drift and completeness checks remain a
separate planned translation gate.

## External Integration Boundary

Default CI explicitly disables:

- storage integration tests
- MailHog integration tests
- asynchronous MailHog and Celery integration tests

It does not start:

- MinIO
- MailHog
- Redis
- Celery Worker
- Celery Beat

Those integrations remain opt-in and are documented by their owning runtime
and testing documents.

## Planned Gates

Later Phase 4 stages will add separate jobs for:

- translation integrity
- workflow YAML validation
- formatting, linting, and import ordering
- incremental typing
- Markdown and local-link validation
- dependency security auditing

Each job should remain independently diagnosable and should be enabled only
after the repository has a clean reproducible baseline for that gate.
