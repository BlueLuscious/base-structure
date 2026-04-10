# Tenancy App

This document explains the purpose and structure of the `tenancy/` app and the active-tenant flow it owns.

See also:

- `docs/project.md`
- `docs/tenancy/resolution/resolution.md`
- `docs/core/core.md`
- `docs/core/adminsites/adminsites.md`
- `docs/core/config/storage/storage.md`
- `docs/accounts/accounts.md`

## Goal

`tenancy/` provides the root multitenancy domain used to scope business data across the project.

It currently defines:

- the base tenant entity
- tenant branding assets and display metadata
- tenant-to-user memberships
- tenant-to-group bindings
- role choices for tenant memberships
- typed query infrastructure for tenant data
- request-time active tenant resolution
- explicit active-tenant switching
- tenant-scoped access policies
- owner-admin business settings helpers
- master admin registrations for technical administration

`tenancy/` owns both:

- tenant persistence
- active-tenant request behavior

Tenant persistence and active-tenant runtime behavior are documented together here because they belong to the same app boundary.

## Current Structure

Current contents:

- `apps.py`
- `constants.py`
- `urls.py`
- `choices/`
- `models/`
- `access/`
- `resolution/`
- `switching/`
- `session/`
- `runtime/`
- `middleware/`
- `views/`
- `admin/`
- `migrations/`
- `tests/`

The current package groups two related concerns:

- persistence and membership rules
- request-time tenant context

The app also contains owner-admin tenant settings helpers because those screens are tenant-domain behavior, even when they are mounted inside the shared owner admin site.

## Responsibilities

The `tenancy/` app is responsible for:

- defining the root tenant entity
- defining how users belong to tenants
- exposing reusable tenant query helpers
- exposing shared request-time tenant resolution helpers
- exposing shared tenant access policies
- owning the active-tenant request flow end to end
- exposing owner-facing business settings flows for the active tenant
- registering tenant infrastructure in the master admin site

It is also the current home for tenant-aware request utilities because those utilities are tightly coupled to:

- `TenantModel`
- `TenantMembershipModel`
- tenant-scoped request resolution

## Models

### `TenantModel`

`TenantModel` is the root business scope entity for the project.

Current fields cover:

- UUID primary key
- human-friendly tenant name
- unique slug
- active flag
- audit timestamps

Current intent:

- tenants should be introduced before domain apps start depending on them
- later domain models can reference `TenantModel` directly once multitenancy is wired through the rest of the project

### `TenantMembershipModel`

`TenantMembershipModel` links one user to one tenant.

Current fields cover:

- relation to `TenantModel`
- relation to `UserModel`
- membership role
- active flag
- primary-tenant flag
- audit timestamps

Current intent:

- a user may belong to multiple tenants
- each user should have at most one primary tenant membership
- tenant-specific roles should live on the membership rather than directly on the user model

### `TenantBrandingModel`

`TenantBrandingModel` stores reusable visual identity data for one tenant.

Current fields cover:

- relation to `TenantModel`
- optional display name
- light and dark logo variants
- light and dark icon variants
- light and dark favicon variants
- audit timestamps

Current intent:

- keep branding out of `TenantModel`
- reuse the same branding data across admin and future frontend surfaces
- let tenant-aware media storage place branding uploads under the active tenant path when one exists
- let the owner admin resolve light and dark favicon variants from branding, with final theme-specific selection handled by a small admin-side script

### `TenantGroupModel`

`TenantGroupModel` links one Django auth group to one tenant.

Current fields cover:

- relation to `TenantModel`
- relation to Django `Group`
- audit timestamps

Current intent:

- groups remain compatible with Django auth
- tenant ownership of groups stays explicit
- future owner-facing group visibility and assignment can be scoped by the active tenant

## Choices

The app keeps membership roles outside the model.

Current choice enum:

- `TenantRole`

Current values:

- `master`
- `owner`
- `operator`

## Active Tenant Resolution

The base structure now resolves an active tenant during the request cycle.

Current behavior:

- resolution happens through `ActiveTenantMiddleware`
- middleware lives in `tenancy/middleware/`
- resolution rules live in `tenancy/resolution/`
- session persistence lives in `tenancy/session/`
- runtime request context lives in `tenancy/runtime/`
- the active tenant is stored in session
- if the session does not define one, the request falls back to the user's primary active membership
- if no primary membership exists, the first active membership is used
- the active tenant is also exposed through a runtime context helper for request-bound infrastructure such as media storage

Current request contract:

- `request.tenant` contains the resolved tenant or `None`

This keeps tenant-aware admin and future tenant-aware web flows grounded in one shared base mechanism.

Request-aware storage behavior that consumes the runtime active tenant is documented in:

- `docs/core/config/storage/storage.md`

The detailed structure, strategy contract, and future path or host resolution options are documented in:

- `docs/tenancy/resolution/resolution.md`

## Explicit Tenant Switching

The base structure now supports explicit tenant switching.

Current behavior:

- the app exposes `switch-active-tenant` through `tenancy/urls.py`
- it stores the selected tenant in session
- it validates that the authenticated user still has one active membership for the requested tenant
- it redirects back to a safe `next` URL when provided

Current intent:

- session state controls the current tenant context
- the primary membership remains the fallback default
- switching the active tenant does not rewrite `is_primary`

## Use Cases

Current concrete use cases:

- attach users to one or more tenants
- attach Django groups to one tenant
- assign tenant roles such as `owner` and `operator` to support users
- choose the active tenant during owner-admin work
- display tenant-aware owner admin metadata such as title and header
- switch tenant context explicitly from the owner admin dropdown
- let active tenant owners update tenant branding from the owner admin business settings screen
- prefix uploaded media under `tenants/<tenant-slug>/...`

These are internal or admin-facing use cases.
The project does not yet expose a tenant-aware public frontend flow.

## Future Direction

The current implementation is intentionally centered on session-backed resolution because it fits the owner admin flow.

Future frontend work may require path-based or host-based tenant resolution without changing the current admin URL shape.

The detailed resolution roadmap, strategy breakdown, and future examples are documented in:

- `docs/tenancy/resolution/resolution.md`

## Access Policies

`tenancy/access/` now separates tenant authorization into small policy objects.

Current policy split:

- `TenantAccessPolicy`
- `TenantAccountsAccessPolicy`

### `TenantAccessPolicy`

This is the base policy for tenant membership and role checks.

Current responsibilities:

- verify whether a user belongs to one tenant
- verify whether a user has one tenant role
- verify whether a user may manage a tenant as an active `owner`

This policy should stay generic and reusable across apps that need tenant membership checks.

### `TenantAccountsAccessPolicy`

This is the `accounts/`-specific tenant policy.

Current responsibilities:

- verify whether the current request may manage owner-scoped accounts
- decide whether one user is visible inside owner `Users`
- decide whether one group is visible inside owner `Groups`

This keeps the reusable tenant-role checks in the base policy while keeping tenant-scoped authorization inside `tenancy/`, even when the current consumer surface is `accounts/`.

## Policy Direction For Future Apps

The current policy split is intended to scale in two layers:

- `TenantAccessPolicy` stays as the reusable tenant-membership and tenant-role base policy
- app-specific policies should sit on top only when one domain needs stricter rules than the generic tenant-member flow

Current architectural direction:

- `accounts` and `tenancy` remain owner-only surfaces
- future owner-managed apps may allow active tenant members such as `operator` to access the app when they both:
  - belong to the active tenant
  - hold the required Django permissions through tenant-scoped groups or direct user permissions

This means `TenantAccessPolicy` remains the base reusable policy layer, while future app-specific policies should only appear when one domain needs stricter rules than the generic tenant-member plus Django-permission pattern.

For the concrete owner-admin wiring checklist for future apps, see:

- `docs/core/adminsites/adminsites.md`

## Relationship With `accounts/`

`UserModel` keeps the authentication identity.

`tenancy/` adds tenant scope on top through:

- `TenantMembershipModel`
- `UserModel.tenants` using a through model

This keeps authentication and tenant membership related, but not collapsed into the same model.

## Admin

Current master registrations:

- `TenantModelAdmin`
- `TenantGroupModelAdmin`
- `TenantMembershipModelAdmin`

These registrations exist so the multitenancy base can be inspected and administered from the technical admin surface before the owner-facing tenant flows are defined.

The shared site classes and project admin wiring live in:

- `docs/core/adminsites/adminsites.md`

## Tests

The app already follows the project test structure convention.

Current test areas:

- `tenancy/tests/access/`
- `tenancy/tests/resolution/`
- `tenancy/tests/models/`
- `tenancy/tests/querysets/`
- `tenancy/tests/managers/`
- `tenancy/tests/middleware/`
- `tenancy/tests/views/`

## What Should Live Here

Good candidates:

- tenant identity
- tenant membership rules
- tenant query helpers
- future tenant-scoped infrastructure that belongs to the multitenancy layer itself
- request-time tenancy infrastructure tightly coupled to tenant membership and active-tenant behavior

## What Should Not Live Here

Avoid placing app-specific domain logic in this app.

Examples:

- catalog business rules
- quotation lifecycle rules
- cart behavior
- project-wide admin infrastructure

Those concerns belong in:

- `docs/core/core.md`
- `docs/core/adminsites/adminsites.md`
