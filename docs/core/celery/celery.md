# Celery

This document explains the project-wide Celery wiring under `core/celery.py`.

See also:

- `docs/project.md`
- `docs/core/core.md`
- `docs/core/celery/tasks/tasks.md`
- `docs/core/mail/mail.md`

## Goal

The Celery layer exists to provide one reusable asynchronous task runtime for the whole project.

It should:

- stay project-wide instead of mail-only
- use Redis as the shared local broker infrastructure
- keep the Celery bootstrap in `core/`
- allow future apps to add background tasks without reinventing the async stack

## Current Scope

The current implementation provides:

- one project Celery app in `core/celery.py`
- Django-settings-based Celery configuration
- Redis-backed broker and result backend settings
- autodiscovery for future app-level `tasks.py` modules

The current runtime does not yet include real Celery task usage.

The first planned async use case is outbound mail, but the stack is intentionally general-purpose.

## Project Files

Current files:

- `core/celery.py`

## Current Settings Direction

Celery reads its configuration from `core/settings.py` through the `CELERY_` namespace.

Current environment-driven settings:

- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `CELERY_TASK_ALWAYS_EAGER`

Current default behavior:

- broker defaults to `REDIS_URL`
- result backend defaults to `REDIS_URL`
- tasks use JSON serialization
- broker retry on startup stays enabled
- eager mode is available for opt-in local or test scenarios

## Local Development

Redis is expected to be available locally through Docker:

- `127.0.0.1:6379`

Example local values:

- `REDIS_URL=redis://127.0.0.1:6379/0`
- `CELERY_BROKER_URL=redis://127.0.0.1:6379/0`
- `CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0`

Example worker command:

```powershell
.\.venv\Scripts\celery.exe -A core.celery worker --loglevel=info
```

## Ownership Rule

Keep the Celery bootstrap in `core/`.

Keep future domain task definitions close to the app that owns the business flow unless they are truly project-wide.

Examples:

- project-wide async infrastructure belongs in `core/`
- app-owned business tasks should prefer living in the app that owns that workflow

For shared task placement and payload conventions, see:

- `docs/core/celery/tasks/tasks.md`

## Future Direction

The next steps expected on top of this wiring are:

1. wire async mail delivery as the first real use case
2. document the first real task implementations on top of the shared conventions
