# Project Documentation Map

This directory contains the main architectural and operational documentation for the project.

Use this file first to understand where each topic is documented and which document owns each concern.

## Current Documented Scope

The runtime code currently documented here is centered on:

- `accounts/`
- `tenancy/`
- `core/`
- `front/` as a future-facing integration surface

Other domain apps may exist as future work or on other branches, but they are not the primary documented runtime scope here.

Current status of the other app folders:

- `front/` exists as the intended UI surface for future reusable components and tenant-aware routes, but it is not part of the current runtime app scope wired by `core/settings.py`
- `catalog/`, `cart/`, `masterdata/`, and `quotation/` are present as placeholders for future domain work and do not yet define the main documented runtime scope

## Project Entry Docs

- Repository setup and development workflow: `README.md`
- Capability status by implementation stage: `docs/capability-status.md`

## Core Docs

- Project package overview: `docs/core/core.md`
- Project admin infrastructure: `docs/core/adminsites/adminsites.md`
- Project configuration overview: `docs/core/config/config.md`
- Project mail infrastructure: `docs/core/mail/mail.md`
- Mail composer guidance: `docs/core/mail/composers/composers.md`
- Storage configuration details: `docs/core/config/storage/storage.md`

## App Docs

- Accounts app: `docs/accounts/accounts.md`
- Front app and future tenant-aware UI direction: `docs/front/front.md`
- Tenancy app: `docs/tenancy/tenancy.md`
- Tenancy resolution layer: `docs/tenancy/resolution/resolution.md`

## Ownership Rule

To avoid repeating the same explanation in multiple places:

- `docs/core/core.md` owns the explanation of what belongs in `core/`
- `docs/core/adminsites/adminsites.md` owns admin site infrastructure details
- `docs/core/config/config.md` owns the configuration-layer boundary
- `docs/core/mail/mail.md` owns the project-wide outbound mail service
- `docs/core/mail/composers/composers.md` owns composer usage and design guidance for the project mail stack
- `docs/core/config/storage/storage.md` owns storage provider and env-var details
- `docs/accounts/accounts.md` owns the `accounts/` domain structure
- `docs/front/front.md` owns the frontend structure and future tenant-aware UI direction
- `docs/tenancy/tenancy.md` owns the `tenancy/` domain structure
- `docs/tenancy/resolution/resolution.md` owns the active-tenant resolution design and strategy layer

When one topic depends on another, the app or subsystem doc should link to the owning document instead of duplicating the full explanation.
