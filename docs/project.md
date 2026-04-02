# Project Documentation Map

This directory contains the main architectural and operational documentation for the project.

Use this file first to understand where each topic is documented and which document owns each concern.

## Current Documented Scope

The runtime code currently documented here is centered on:

- `accounts/`
- `tenancy/`
- `core/`

Other domain apps may exist as future work or on other branches, but they are not the primary documented runtime scope here.

## Project Entry Docs

- Repository setup and development workflow: `README.md`
- Branch-local backlog and postponed decisions: `docs/pending-tasks.md`

## Core Docs

- Project package overview: `docs/core/core.md`
- Project admin infrastructure: `docs/core/adminsites/adminsites.md`
- Project configuration overview: `docs/core/config/config.md`
- Storage configuration details: `docs/core/config/storage/storage.md`

## App Docs

- Accounts app: `docs/accounts/accounts.md`
- Tenancy app: `docs/tenancy/tenancy.md`
- Tenancy resolution layer: `docs/tenancy/resolution/resolution.md`

## Ownership Rule

To avoid repeating the same explanation in multiple places:

- `docs/core/core.md` owns the explanation of what belongs in `core/`
- `docs/core/adminsites/adminsites.md` owns admin site infrastructure details
- `docs/core/config/config.md` owns the configuration-layer boundary
- `docs/core/config/storage/storage.md` owns storage provider and env-var details
- `docs/accounts/accounts.md` owns the `accounts/` domain structure
- `docs/tenancy/tenancy.md` owns the `tenancy/` domain structure
- `docs/tenancy/resolution/resolution.md` owns the active-tenant resolution design and strategy layer
- `docs/pending-tasks.md` owns branch-local backlog items, not architectural truth

When one topic depends on another, the app or subsystem doc should link to the owning document instead of duplicating the full explanation.
