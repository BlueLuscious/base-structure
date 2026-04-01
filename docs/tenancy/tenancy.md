# Tenancy App

This document explains the purpose and structure of the `tenancy/` app.

## Goal

`tenancy/` provides the root multitenancy domain used to scope business data across the project.

It currently defines:

- the base tenant entity
- tenant-to-user memberships
- role choices for tenant memberships
- typed query infrastructure for tenant data
- master admin registrations for technical administration

The app should remain focused on tenant identity and membership scope.

## Current Structure

Current contents:

- `apps.py`
- `choices/`
- `models/`
- `admin/`
- `migrations/`
- `tests/`

## Responsibilities

The `tenancy/` app is responsible for:

- defining the root tenant entity
- defining how users belong to tenants
- exposing reusable tenant query helpers
- registering tenant infrastructure in the master admin site

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

## Tests

The app already follows the project test structure convention.

Current test areas:

- `tenancy/tests/models/`
- `tenancy/tests/querysets/`

## What Should Live Here

Good candidates:

- tenant identity
- tenant membership rules
- tenant query helpers
- future tenant-scoped infrastructure that belongs to the multitenancy layer itself

## What Should Not Live Here

Avoid placing app-specific domain logic in this app.

Examples:

- catalog business rules
- quotation lifecycle rules
- cart behavior
- project-wide admin infrastructure
