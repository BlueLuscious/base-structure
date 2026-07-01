# Core Configuration

This document explains the purpose of `core/config/` and how configuration modules should be organized there.

See also:

- `docs/project.md`
- `docs/core/core.md`
- `docs/core/config/logging/logging.md`
- `docs/core/config/logging/usage.md`
- `docs/core/config/storage/storage.md`
- `docs/core/config/storage/testing.md`

## Goal

`core/config/` exists to keep `core/settings.py` readable while still allowing structured, testable, environment-driven configuration code.

Use this package for configuration that is:

- project-wide
- environment-dependent
- reused by multiple settings values
- easier to maintain when isolated from the main settings file

## Current Structure

Current contents:

- `environment/`
- `logging/`
- `storage/`

The `environment/` package contains shared strict parsing and relationship
validation for environment-driven settings.

The `logging/` package contains configuration logic for:

- project-wide logger settings
- environment-driven log levels
- shared Django and Celery logging defaults

The `storage/` package contains configuration logic for:

- media storage
- staticfiles storage
- shared storage helpers

See:

- `docs/core/config/storage/storage.md`
- `docs/core/config/storage/testing.md`

This document owns the boundary of the configuration layer.
Detailed provider behavior, environment variables, and storage combinations belong in the storage-specific document instead of being repeated here.

## Environment Contract

`.env.example` is the complete copyable local-development contract. Values in
that file are neutral development defaults, not production credentials.

Environment values use these parsing rules:

- booleans accept `1`, `true`, `yes`, and `on`
- booleans accept `0`, `false`, `no`, and `off`
- boolean matching is case-insensitive
- unsupported booleans raise `ImproperlyConfigured` and name the variable
- numeric values raise `ImproperlyConfigured` instead of an unlabelled
  conversion error
- integration-test timeout and polling values must be finite and greater than
  zero

### Variable Ownership

| Concern | Variables | Owning document |
| --- | --- | --- |
| Django security and runtime | `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `TIME_ZONE` | This document |
| Database | `DATABASE_URL`, `DB_SCHEMA` | This document |
| Logging | `LOG_LEVEL`, `DJANGO_LOG_LEVEL`, `CELERY_LOG_LEVEL` | `docs/core/config/logging/logging.md` |
| Media, staticfiles, S3, R2, and storage tests | `MEDIAFILES_*`, `STATICFILES_*`, `AWS_*`, `CLOUDFLARE_R2_ACCOUNT_ID`, `RUN_STORAGE_INTEGRATION_TESTS` | `docs/core/config/storage/storage.md` |
| Mail and MailHog tests | `EMAIL_*`, `DEFAULT_FROM_EMAIL`, `RUN_MAIL_INTEGRATION_TESTS`, `RUN_ASYNC_MAIL_INTEGRATION_TESTS`, `MAILHOG_*` | `docs/core/mail/runtime.md` |
| Redis and Celery | `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CELERY_TASK_ALWAYS_EAGER` | `docs/core/celery/celery.md` |
| Compose infrastructure | `POSTGRES_*`, `MINIO_*`, `MAILHOG_*`, `REDIS_PORT` | `docs/project.md` |

`LANGUAGE_CODE` remains English and the supported language list remains English
and Spanish in tracked settings. Supported languages are not environment-driven
because they must agree with available translation catalogs.

`TIME_ZONE` is environment-driven and defaults to the neutral `UTC` value.
`USE_I18N` and `USE_TZ` remain architectural settings in code.

## Validation And Deployment

Normal startup accepts documented development defaults. Invalid values that
cannot be parsed fail immediately with an actionable configuration error.

`EMAIL_USE_TLS` and `EMAIL_USE_SSL` are mutually exclusive. Enabling both stops
settings construction and identifies the conflicting variables.

Production configuration must replace the development secret and credentials,
disable debug mode, and define the real allowed hosts and trusted origins.
Validate production-intended environment values with:

```bash
python manage.py check --deploy
```

Django's deployment checks are the production gate. Custom project checks
should be added only when a project contract is not covered by Django.

## Dependency Contract

Dependency ownership is split between:

- `requirements.in`: reviewed direct runtime dependencies
- `requirements.txt`: generated, fully pinned runtime dependency lock
- `requirements-dev.in`: reviewed direct development and quality dependencies
- `requirements-dev.txt`: generated, fully pinned development-tool lock

Compile the lock after reviewing direct dependency changes:

```bash
python -m pip install pip-tools
python -m piptools compile --output-file=requirements.txt requirements.in
```

Install or synchronize the environment from the lock:

```bash
python -m pip install -r requirements.txt
```

Compile and install the development-tool lock:

```bash
python -m piptools compile --output-file=requirements-dev.txt requirements-dev.in
python -m pip install -r requirements-dev.txt
```

The development lock uses the runtime lock as a constraint. Install both locks
when one local workflow needs the Django runtime and quality tools together.

The base intentionally owns these optional-capability dependencies:

- `boto3` and `django-storages` for S3-compatible storage
- `django-import-export` for admin import and export
- `django-components` for the designed reusable UI layer
- `celery` and `redis` for asynchronous execution
- `whitenoise` for local static-file serving in supported deployment shapes

`psycopg[binary]` expresses one PostgreSQL driver decision in
`requirements.in`. The generated lock contains both `psycopg` and its binary
implementation as resolved packages.

The first development-only dependency is yamllint, which validates Compose and
GitHub workflow YAML without becoming a runtime application dependency.
Automated updates and security auditing remain Phase 4 quality-gate work.

## What Belongs In `core/config/`

Good candidates:

- configuration builders
- environment parsing helpers
- provider resolution
- settings-related adapter selection

Examples:

- selecting a storage provider from env vars
- building `STORAGES`
- deciding extra installed apps or middleware based on configuration

## What Does Not Belong In `core/config/`

Avoid placing these here:

- domain business logic
- model behavior
- view logic
- app-specific concerns that belong in a domain app

Also avoid turning `core/config/` into a miscellaneous utilities package.

## Design Guidelines

Prefer:

- small focused modules
- explicit contracts
- environment-driven configuration
- shared helpers only when the logic is truly shared

Avoid:

- giant builders that mix unrelated concerns
- hidden side effects
- configuration code that silently mutates global state

## Relationship With `settings.py`

`settings.py` should consume configuration from `core/config/`, not reimplement it inline.

The intended pattern is:

- `settings.py` imports a builder or public API
- `core/config/` resolves the environment and returns structured values

This keeps settings readable and makes the configuration layer easier to test.

The project currently keeps one `core/settings.py`. Logging, storage, and
environment parsing already have focused configuration boundaries, so separate
base, development, test, and production settings modules would add complexity
without improving the supported workflow.

## Maintenance Rule

If a configuration area becomes large enough to deserve its own boundary, create a dedicated subpackage inside `core/config/` rather than growing a single module indefinitely.
