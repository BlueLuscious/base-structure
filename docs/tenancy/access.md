# Tenancy Access

This document explains the tenant-scoped access policies owned by `tenancy/`.

See also:

- `docs/project.md`
- `docs/tenancy/tenancy.md`
- `docs/core/adminsites/adminsites.md`
- `docs/core/adminsites/owner-managed-apps.md`
- `docs/accounts/accounts.md`

## Goal

The access layer exists to keep tenant membership and tenant-scoped authorization rules explicit and reusable.

It should:

- centralize tenant membership checks
- centralize tenant role checks
- support owner-only flows where required
- give future apps one reusable base policy instead of ad hoc role checks

## Current Policy Split

`tenancy/access/` currently separates tenant authorization into small policy objects.

Current policies:

- `TenantAccessPolicy`
- `AccountsAccessPolicy`

## `TenantAccessPolicy`

This is the base policy for tenant membership and role checks.

Current responsibilities:

- verify whether a user belongs to one tenant
- verify whether a user has one tenant role
- verify whether a user may manage a tenant as an active `owner`

This policy should stay generic and reusable across apps that need tenant membership checks.

## Role And Admin Boundaries

Tenant roles and Django administrative authority are related but remain
separate checks:

- `OWNER` grants tenant-management authority for owner-only surfaces
- `OPERATOR` represents an active tenant member whose app access also depends
  on Django permissions

Master Admin access depends on `is_superuser`, not on the existence of a
membership. Platform administrators do not need a tenant role and may enter
`/admin/` without belonging to a tenant.

Owner Admin manages `OWNER` and `OPERATOR` memberships only.

### Neutral End-To-End Example

Consider one `Example Business` tenant:

1. A platform administrator with `is_superuser=True` enters `/admin/`.
   Tenant membership is not required.
2. A staff user with an active `OWNER` membership for `Example Business`
   enters `/owner-admin/`.
   They can manage tenant settings and may manage users or groups only when
   the corresponding Django permissions are also assigned.
3. A staff user with an active `OPERATOR` membership may enter the owner admin
   shell, but cannot manage tenant settings or accounts. Future domain apps may
   grant that operator access through active membership plus app-specific
   Django permissions.

Neither an `OWNER` nor `OPERATOR` membership grants access to `/admin/`.
Platform authority remains exclusively represented by `is_superuser`.

## Current Owner-Admin Isolation Matrix

Existing owner-managed registrations apply these boundaries:

| Boundary | Users | Groups | Business settings |
| --- | --- | --- | --- |
| Sidebar visibility | Owner role and Django view permission | Owner role and Django view permission | Owner role |
| Queryset | Active tenant memberships with owner-visible roles | Active tenant group binding | Active tenant primary key |
| Form choices | Active-tenant groups and membership roles | Permissions held by the acting owner | Active-tenant branding inline |
| Object access | Active-tenant membership and Django permission | Active-tenant group binding and Django permission | Object must equal active tenant |
| Write behavior | Membership inline is bound to active tenant | New group receives active-tenant binding | Add and delete are disabled |

The matrix is enforced by the current policy, admin, form, formset, and
sidebar tests. New owner-managed apps must establish the same boundaries for
their own objects rather than inheriting this matrix implicitly.

## `AccountsAccessPolicy`

This is the `accounts/`-specific policy now owned by `accounts/`.

Current responsibilities:

- verify whether the current request may manage owner-scoped accounts
- decide whether one user is visible inside owner `Users`
- decide whether one group is visible inside owner `Groups`

This keeps the reusable tenant-role checks in the base tenancy policy while moving `accounts`-specific authorization into the `accounts/` domain that actually consumes it.

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

- `docs/core/adminsites/owner-managed-apps.md`

## Relationship With `accounts/`

`accounts/` consumes tenant authorization through these two layers:

- `TenantAccessPolicy` for base tenant-membership and role checks
- `AccountsAccessPolicy` for `accounts`-specific visibility and management rules

This stricter owner-only rule is intentional for `accounts`.

Future tenant-aware apps should not copy the `accounts` flow by default.
`accounts` stays stricter because it manages support users, memberships, and tenant-scoped permission groups.

## Current Logging Direction

The access layer should stay relatively quiet.

Current direction:

- prefer logging runtime boundaries that consume access outcomes instead of logging every policy decision
- only add policy-level logs when one real operational blind spot appears

This keeps the access layer reusable without turning every permission check into console noise.

## What Should Live Here

Good candidates:

- reusable tenant membership checks
- reusable tenant role checks
- small app-specific tenant access policies when one app truly needs stricter rules than the base flow

## What Should Not Live Here

Avoid placing these here:

- request-time tenant resolution logic
- session switching logic
- owner-admin infrastructure rules that belong in `core/adminsites/`

Those concerns belong in:

- `docs/tenancy/runtime.md`
- `docs/tenancy/resolution.md`
- `docs/core/adminsites/adminsites.md`
