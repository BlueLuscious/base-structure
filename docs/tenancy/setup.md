# Initial Tenant Setup

This document owns the minimum manual procedure for creating the first tenant
and owner-admin access in a new project.

The base does not provide a special bootstrap command. Initial tenant data is
created through the technical admin so the setup remains explicit and uses the
same models and validation as later administration.

## Prerequisites

Before creating tenant data:

1. apply the tracked migrations
2. create an active Django superuser
3. start Django
4. sign in to `/admin/`

The repository README owns the complete first-run sequence.

## Create The First Tenant And Owner

From the technical admin:

1. Create an active business under `Tenancy > Businesses`.
2. Create an active user under `Accounts > Users`.
3. Enable `Staff status` for that user so they may enter an admin site.
4. Create a business access record under `Tenancy > Business access`.
5. Select the business and user created above.
6. Choose the `Owner` role.
7. Keep the access active.
8. Mark it as primary so membership fallback resolves this business
   automatically.
9. Assign the Django model permissions needed by that owner.

The owner can then sign in to `/owner-admin/`.

The owner role grants tenant-management authority, but it does not replace
Django model permissions for owner-managed app sections.

## Multiple Tenants

A user may have access to multiple active tenants, but may have only one
primary membership. The primary tenant is the automatic fallback when no valid
tenant has been selected in the session.

The owner-admin tenant switcher can select another accessible tenant after the
initial setup is complete.

## Verification

The default test suite includes smoke coverage that verifies:

- the technical admin renders for an active superuser
- the owner admin renders for an active staff owner whose active primary
  membership resolves the expected tenant

Request-time resolution and authorization details are documented in:

- `docs/tenancy/runtime.md`
- `docs/tenancy/access.md`
- `docs/tenancy/resolution.md`
