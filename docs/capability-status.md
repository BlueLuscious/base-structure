# Capability Status Map

This document classifies the reusable base capabilities by implementation
status.

See also:

- `docs/project.md`

## Status Definitions

- `Implemented`: active code is present in the current runtime.
- `Extension point`: supporting code exists, but the optional path is not active.
- `Designed for future`: documentation defines a direction with no current runtime
  implementation.

## Implemented

### Accounts And Authentication

- custom `UserModel`
- typed manager and queryset foundations
- master and owner admin registrations for users and groups
- tenant-scoped owner account management

Read:

- `docs/accounts/accounts.md`
- `docs/core/adminsites/adminsites.md`

### Tenancy

- tenant, membership, tenant-group, and branding models
- session-first active-tenant resolution with membership fallback
- request middleware and runtime tenant context
- explicit owner-admin tenant switching
- owner-facing tenant settings and branding

Read:

- `docs/tenancy/tenancy.md`
- `docs/tenancy/runtime.md`
- `docs/tenancy/resolution.md`
- `docs/tenancy/access.md`

### Administration

- separate master and owner admin sites
- Unfold integration
- tenant-aware owner metadata, navigation, and branding
- light and dark owner favicon support
- django-import-export integration installed at project level

No app-owned import/export resource is included yet.

Read:

- `docs/core/adminsites/adminsites.md`
- `docs/core/adminsites/owner-managed-apps.md`

### Storage

- local, S3, and R2 media adapters
- local, WhiteNoise, S3, and R2 static-file adapters
- tenant-aware media object paths
- opt-in external storage integration tests

Read:

- `docs/core/config/storage/storage.md`
- `docs/core/config/storage/testing.md`

### Mail

- synchronous and asynchronous delivery
- raw and template-based message services
- DTO, serializer, renderer, composer, policy, and backend layers
- shared HTML and text layouts
- tenant-aware template context and reply behavior
- opt-in MailHog integration tests

Read:

- `docs/core/mail/mail.md`
- `docs/core/mail/runtime.md`
- `docs/core/mail/templates.md`
- `docs/core/mail/composers.md`

### Asynchronous Runtime

- Redis-backed Celery configuration
- Worker and Beat bootstrap
- code-owned Beat schedule builder
- asynchronous mail tasks
- app-owned task conventions

The Beat schedule is intentionally empty until a real recurring task exists.

Read:

- `docs/core/celery/celery.md`
- `docs/core/celery/tasks/tasks.md`

### Development Infrastructure

- PostgreSQL, MinIO, MailHog, and Redis through Docker Compose
- host-run Django, Celery Worker, and Celery Beat
- environment examples for supported storage combinations
- optional Discord repository notifications

Read:

- `README.md`
- `docs/github/workflows/discord.md`

## Extension Points

### Reusable Component Runtime

`django-components` is installed and wired into templates, static discovery,
and project URLs. No `front/` app or reusable component tree currently
consumes it.

Read:

- `docs/core/config/config.md`
- `docs/front/front.md`

### Path-Based Tenant Resolution

`PathTenantResolutionStrategy` exists but always returns `None` and is not part
of the active resolver chain. It is reserved for a future tenant-aware public
surface.

Read:

- `docs/tenancy/resolution.md`
- `docs/front/front.md`

### Owner-Managed Domain Apps

The access and admin wiring contract exists for future tenant-scoped apps.
There is no business-domain app in the current repository.

Read:

- `docs/core/adminsites/owner-managed-apps.md`
- `docs/tenancy/access.md`

### Import/Export Resources

The dependency and Unfold integration are installed, but no model-specific
resource is currently implemented. Future resources belong to the app that owns
their model.

Read:

- `docs/core/adminsites/adminsites.md`

## Designed For Future

### Front App And Public UI

No `front/` package, public page, or reusable component tree currently exists.
`front/` remains the designed project path for reusable components, pages,
frontend views, assets, sandbox examples, and future public routes.

Read:

- `docs/front/front.md`

### Host-Based Tenancy

Host or subdomain tenant resolution is not implemented.

Read:

- `docs/tenancy/resolution.md`

### Business-Domain Apps

No catalog, cart, quotation, master-data, or other product-specific app is part
of this base. Derived projects should introduce only the domains they need and
follow the app, tenancy, admin, task, test, translation, and documentation
contracts described by this repository.

## Maintenance Rule

When capability status changes:

1. update the code-owning document
2. update this status map
3. update `docs/project.md` when navigation or ownership changes
4. keep branch-local planning outside committed project documentation
