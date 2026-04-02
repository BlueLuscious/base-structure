# Accounts App

This document explains the purpose and structure of the `accounts/` app.

See also:

- `docs/project.md`
- `docs/core/core.md`
- `docs/core/adminsites/adminsites.md`
- `docs/tenancy/tenancy.md`

## Goal

`accounts/` provides the authentication domain for the project.

It currently defines the custom Django user model and the first admin registrations required to manage authentication data inside the project admin sites.

## Current Structure

Current contents:

- `apps.py`
- `models/`
- `admin/`
- `migrations/`
- `tests/`

## Responsibilities

The `accounts/` app is responsible for:

- defining the project's user model
- exposing user query infrastructure
- registering authentication-related admins where needed

It should remain focused on authentication and account-level concerns.

## Models

### `UserModel`

`UserModel` extends Django's `AbstractUser` and acts as the project's `AUTH_USER_MODEL`.

Current behavior:

- preserves Django auth compatibility
- exposes a typed custom manager
- keeps tenant membership separate through the tenancy layer

Related files:

- `accounts/models/user_model.py`
- `accounts/models/managers/user_model_manager.py`
- `accounts/models/querysets/user_model_queryset.py`

## Manager and QuerySet

The app follows the project model structure convention:

- model
- queryset
- manager

Current pieces:

- `UserModelQuerySet`
- `UserModelManager`

At the moment the queryset layer is intentionally small, but the structure is already in place for reusable account filters and query helpers.

## Relationship With `tenancy/`

`accounts/` keeps authentication identity.

`tenancy/` adds business scope on top through:

- `UserModel.tenants`
- `TenantMembershipModel`

This keeps user identity and tenant membership related, but not collapsed into one model.

## Admin

The app already integrates with the custom project admin site structure.

Current registrations live in:

- `accounts/admin/master/`
- `accounts/admin/owner/`

Current master registrations:

- `UserModelAdmin`
- `GroupAdmin`

Current owner registrations:

- `OwnerUserModelAdmin`
- `OwnerGroupAdmin`

These admins are registered against the shared project admin sites:

- `master_admin_site`
- `owner_admin_site`

This keeps authentication administration visible in the right site while following the project rule of keeping domain admin logic inside each app.

For the owner admin flow:

- users remain owner-managed support accounts
- only users with an active `owner` membership for the active tenant may manage `Users` and `Groups`
- owner-visible users are scoped to users that belong to the active tenant
- the user screen exposes the active-tenant membership inline so owners can switch a person between `owner` and `employee`
- groups are scoped to the active tenant through `TenantGroupModel`
- user group assignment is filtered to groups that belong to the active tenant
- group permissions are filtered to the permissions already held by the current owner

The current owner admin flow consumes tenant authorization through two policy layers owned by `tenancy/`:

- `TenantAccessPolicy` for base tenant-membership and role checks
- `TenantAccountsAccessPolicy` for `accounts`-specific visibility and management rules

The shared site classes, namespace resolution, and Unfold integration are documented in:

- `docs/core/adminsites/adminsites.md`

## Relationship With `core/adminsites/`

`accounts/` should own its admin implementations.

`core/adminsites/` should only provide:

- admin site classes
- shared site instances
- site-level infrastructure

This separation keeps domain admin behavior near the app that owns the models.

## What Should Live Here

Good candidates:

- custom authentication model behavior
- account-specific query helpers
- account-specific admin implementations
- future account DTOs or services if the domain grows

## What Should Not Live Here

Avoid placing unrelated platform infrastructure in this app.

Examples:

- project-wide admin site wiring
- global settings resolution
- storage infrastructure

Those concerns belong in `core/`.
