# Project Documentation Map

This directory contains the architectural and operational documentation for the
reusable Django base.

Use this file to find the document that owns each implemented capability,
extension point, or designed future expansion.

## Current Runtime Scope

The tracked Django packages are:

- `accounts/`: authentication identity and account administration
- `core/`: project settings and shared infrastructure
- `tenancy/`: tenant persistence, access, resolution, and administration

No public frontend or business-domain app is included in the current runtime.

## Designed Future Integration

`front/` is the intended future home for reusable components, public pages,
frontend view infrastructure, and public routes. Its documentation remains
under `docs/front/` so the docs continue to mirror the designed project path.

Catalog, cart, quotation, master-data, and other business-domain apps are not
part of the current tree. They may appear only as clearly labeled examples.

## Project Entry Documents

- Repository setup and development workflow: `README.md`
- Clean-clone verification procedure: `docs/clone-readiness.md`
- Capability status by implementation stage: `docs/capability-status.md`
- Continuous integration quality gates: `docs/github/workflows/ci.md`
- Optional Discord repository notifications: `docs/github/workflows/discord.md`
- VS Code finite task ownership: `docs/vscode/tasks.md`
- VS Code debugger and long-running launch ownership: `docs/vscode/launch.md`

## Core Documentation

- Project package overview: `docs/core/core.md`
- Project-wide Celery runtime: `docs/core/celery/celery.md`
- Celery task conventions: `docs/core/celery/tasks/tasks.md`
- Project admin infrastructure: `docs/core/adminsites/adminsites.md`
- Future owner-managed app wiring: `docs/core/adminsites/owner-managed-apps.md`
- Project configuration overview: `docs/core/config/config.md`
- Project development commands: `docs/core/development/commands/commands.md`
- Project logging configuration: `docs/core/config/logging/logging.md`
- Logging usage rules: `docs/core/config/logging/usage.md`
- Reusable form fields and widgets: `docs/core/forms/forms.md`
- Project mail infrastructure: `docs/core/mail/mail.md`
- Mail runtime behavior: `docs/core/mail/runtime.md`
- Mail template structure: `docs/core/mail/templates.md`
- Mail composer guidance: `docs/core/mail/composers.md`
- Storage configuration details: `docs/core/config/storage/storage.md`
- Storage testing guidance: `docs/core/config/storage/testing.md`

## App Documentation

- Accounts app: `docs/accounts/accounts.md`
- Front app and future public UI direction: `docs/front/front.md`
- Tenancy app: `docs/tenancy/tenancy.md`
- Initial tenant and owner setup: `docs/tenancy/setup.md`
- Tenancy runtime behavior: `docs/tenancy/runtime.md`
- Tenancy access policies: `docs/tenancy/access.md`
- Tenancy resolution layer: `docs/tenancy/resolution.md`

## Local Development Infrastructure

Docker Compose provides PostgreSQL, MinIO, MailHog, and Redis. Django, Celery
Worker, and Celery Beat run from the host development environment.

Default endpoints from `.env.example`:

- PostgreSQL: `127.0.0.1:5432`
- MinIO API: `http://127.0.0.1:9000`
- MinIO console: `http://127.0.0.1:9001`
- MailHog SMTP: `127.0.0.1:1025`
- MailHog web UI: `http://127.0.0.1:8025`
- Redis: `127.0.0.1:6379`

Compose generates container, network, and volume names from the project name.
Inside each Compose network, services retain the stable names `db`, `minio`,
`mailhog`, and `redis`.

Host ports remain configurable so multiple clones can run simultaneously.

Long-running services use `restart: unless-stopped`. The one-shot `minio-mc`
bootstrap does not restart automatically and fails when alias or bucket setup
fails.

PostgreSQL, MinIO, MailHog, and Redis expose health checks where the image
provides the required client. MinIO bootstrap waits for a healthy MinIO server.
The MinIO, MinIO Client, and MailHog images use explicit reviewed versions;
PostgreSQL and Redis retain explicit major-version tracks.

Stop services without removing data:

```bash
docker compose stop
```

Remove containers and networks while retaining the PostgreSQL volume:

```bash
docker compose down
```

Reset the named PostgreSQL volume only when losing local database data is
acceptable:

```bash
docker compose down -v
```

The `minio-data/` bind-mounted directory is independent from named Compose
volumes and is not removed by `docker compose down -v`.

## Ownership Rule

To avoid repeating the same explanation in multiple places:

- `README.md` owns the first-run quick start
- `docs/project.md` owns documentation navigation, local infrastructure, and
  derived-project preparation
- `docs/capability-status.md` classifies implementation status
- `docs/core/core.md` owns the `core/` package boundary
- `docs/core/celery/celery.md` owns the Celery runtime and bootstrap
- `docs/core/celery/tasks/tasks.md` owns task placement and payload conventions
- `docs/core/adminsites/adminsites.md` owns shared admin infrastructure
- `docs/core/adminsites/owner-managed-apps.md` owns future app wiring rules
- `docs/core/config/config.md` owns the configuration boundary
- `docs/core/development/commands/commands.md` owns project development command behavior
- `docs/core/config/logging/logging.md` owns logging construction
- `docs/core/config/logging/usage.md` owns runtime logging rules
- `docs/core/config/storage/storage.md` owns storage provider configuration
- `docs/core/config/storage/testing.md` owns storage integration testing
- `docs/core/forms/forms.md` owns reusable project form fields and widgets
- `docs/core/mail/mail.md` owns the outbound mail package boundary
- `docs/core/mail/runtime.md` owns mail delivery behavior and settings
- `docs/core/mail/templates.md` owns mail layouts and template context
- `docs/core/mail/composers.md` owns composer usage and design
- `docs/accounts/accounts.md` owns the accounts domain
- `docs/front/front.md` owns the designed future frontend direction
- `docs/tenancy/tenancy.md` owns tenant persistence and the app boundary
- `docs/tenancy/setup.md` owns initial tenant and owner setup
- `docs/tenancy/runtime.md` owns request-time tenant behavior
- `docs/tenancy/access.md` owns tenant access policy
- `docs/tenancy/resolution.md` owns tenant resolution strategies
- `docs/github/workflows/ci.md` owns automated project quality gates
- `docs/github/workflows/discord.md` owns optional Discord workflow operation
- `docs/vscode/tasks.md` owns finite local tasks and Compose command usage
- `docs/vscode/launch.md` owns debugger and long-running process usage
- `docs/clone-readiness.md` owns clean-clone verification

When one topic depends on another, link to the owning document instead of
duplicating its full contract.

## Starting A Derived Project

Before using a clone as a new project:

- update repository metadata, Git remotes, and stable display branding
- replace secrets and configure allowed hosts and trusted origins
- choose project-specific database credentials and keep the schema, Compose,
  and Django settings aligned
- select the media and static storage providers
- configure mail delivery, Redis, Celery, language, and timezone
- create the initial superuser, tenant, owner membership, and permissions
- retain, reconfigure, or remove the optional Discord workflow
- review existing migrations before adding project-specific models
- run Django checks, the complete default test suite, translation checks, and
  production deployment checks
