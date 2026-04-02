# Tenancy App

This document explains the purpose and structure of the `tenancy/` app and the active-tenant flow it owns.

See also:

- `docs/project.md`
- `docs/core/core.md`
- `docs/core/adminsites/adminsites.md`
- `docs/core/config/storage/storage.md`
- `docs/accounts/accounts.md`

## Goal

`tenancy/` provides the root multitenancy domain used to scope business data across the project.

It currently defines:

- the base tenant entity
- tenant-to-user memberships
- role choices for tenant memberships
- typed query infrastructure for tenant data
- request-time active tenant resolution
- explicit active-tenant switching
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
- `services/`
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

## Responsibilities

The `tenancy/` app is responsible for:

- defining the root tenant entity
- defining how users belong to tenants
- exposing reusable tenant query helpers
- exposing shared request-time tenant resolution helpers
- owning the active-tenant request flow end to end
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

## Choices

The app keeps membership roles outside the model.

Current choice enum:

- `TenantRole`

Current values:

- `master`
- `owner`

## Active Tenant Resolution

The base structure now resolves an active tenant during the request cycle.

Current behavior:

- resolution happens through `ActiveTenantMiddleware`
- middleware lives in `tenancy/middleware/`
- resolution rules live in `tenancy/services/`
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

### Current Resolution Order

Today the active tenant is resolved in this order:

1. tenant stored in session
2. primary active tenant membership for the authenticated user
3. first active tenant membership for the authenticated user

This is the current behavior used by:

- owner admin metadata
- owner admin tenant switching
- tenant-aware media storage

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
- choose the active tenant during owner-admin work
- display tenant-aware owner admin metadata such as title and header
- switch tenant context explicitly from the owner admin dropdown
- prefix uploaded media under `tenants/<tenant-slug>/...`

These are internal or admin-facing use cases.
The project does not yet expose a tenant-aware public frontend flow.

## Future Direction

The current implementation is intentionally centered on session-backed resolution because it fits the owner admin flow.

Future frontend work may require path-based tenant resolution without changing the current admin URL shape.

Examples of future frontend URL patterns:

- `/t/<tenant-slug>/products/`
- `/t/<tenant-slug>/quotes/`
- `/t/<tenant-slug>/checkout/`

In that future direction:

- admin flows can keep using session-backed tenant switching
- frontend flows can resolve tenant from the path
- both can share the same tenant and membership models

### Target Architecture Direction

This is not implemented yet, but it is the current design target:

- small tenant-resolution strategies
- one composed resolver per context
- admin resolver focused on session plus membership fallback
- frontend resolver focused on path-based resolution

Possible future strategy examples:

- `SessionTenantResolutionStrategy`
- `MembershipTenantResolutionStrategy`
- `PathTenantResolutionStrategy`

Possible future composed resolvers:

- `AdminActiveTenantResolver`
- `FrontendActiveTenantResolver`

The goal is to support multiple resolution styles without turning the current middleware into one large conditional resolver.

## Relationship With `accounts/`

`UserModel` keeps the authentication identity.

`tenancy/` adds tenant scope on top through:

- `TenantMembershipModel`
- `UserModel.tenants` using a through model

This keeps authentication and tenant membership related, but not collapsed into the same model.

## Admin

Current master registrations:

- `TenantModelAdmin`
- `TenantMembershipModelAdmin`

These registrations exist so the multitenancy base can be inspected and administered from the technical admin surface before the owner-facing tenant flows are defined.

The shared site classes and project admin wiring live in:

- `docs/core/adminsites/adminsites.md`

## Tests

The app already follows the project test structure convention.

Current test areas:

- `tenancy/tests/models/`
- `tenancy/tests/querysets/`
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
