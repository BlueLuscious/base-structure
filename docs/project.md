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
- Capability status by implementation stage: `docs/capability-status.md`
- Optional Discord repository notifications: `docs/github/workflows/discord.md`

## Core Documentation

- Project package overview: `docs/core/core.md`
- Project-wide Celery runtime: `docs/core/celery/celery.md`
- Celery task conventions: `docs/core/celery/tasks/tasks.md`
- Project admin infrastructure: `docs/core/adminsites/adminsites.md`
- Future owner-managed app wiring: `docs/core/adminsites/owner-managed-apps.md`
- Project configuration overview: `docs/core/config/config.md`
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
- Tenancy runtime behavior: `docs/tenancy/runtime.md`
- Tenancy access policies: `docs/tenancy/access.md`
- Tenancy resolution layer: `docs/tenancy/resolution.md`

## Ownership Rule

To avoid repeating the same explanation in multiple places:

- `README.md` owns first-run onboarding and clone customization
- `docs/capability-status.md` classifies implementation status
- `docs/core/core.md` owns the `core/` package boundary
- `docs/core/celery/celery.md` owns the Celery runtime and bootstrap
- `docs/core/celery/tasks/tasks.md` owns task placement and payload conventions
- `docs/core/adminsites/adminsites.md` owns shared admin infrastructure
- `docs/core/adminsites/owner-managed-apps.md` owns future app wiring rules
- `docs/core/config/config.md` owns the configuration boundary
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
- `docs/tenancy/runtime.md` owns request-time tenant behavior
- `docs/tenancy/access.md` owns tenant access policy
- `docs/tenancy/resolution.md` owns tenant resolution strategies
- `docs/github/workflows/discord.md` owns optional Discord workflow operation

When one topic depends on another, link to the owning document instead of
duplicating its full contract.
