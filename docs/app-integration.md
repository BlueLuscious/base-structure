# App Integration Guide

This guide defines how a new project app joins the reusable base without
leaving configuration, tenancy, background work, tests, or documentation
partially connected.

Use only the sections required by the app. A plain project-wide app does not
need tenant policy or Celery wiring merely because those extension points
exist.

## Create And Register The App

1. Create the app as a top-level Python package with one clear domain owner.
2. Add its Django app label to `PROJECT_APPS` in `core/settings.py`.
3. Keep `PROJECT_APPS` ordered with the other project-owned packages.
4. Confirm the app configuration uses neutral, translated admin-facing
   metadata when it is shown to users.

`PROJECT_APPS` feeds both `INSTALLED_APPS` and project logger construction.
Do not add the same app independently to both places.

## Logging

The app receives its logger namespace through `PROJECT_APPS`.

Inside the app:

- use `logging.getLogger(__name__)`
- log operational boundaries and actionable fallbacks
- avoid logging secrets, mail bodies, credentials, or tenant-sensitive data
- do not add a separate logging configuration unless the app has a concrete
  handler or level requirement

## Models And Admin

When the app exposes administration:

1. keep admin code inside the owning app
2. register technical administration under `<app>/admin/master/`
3. register tenant-facing administration under `<app>/admin/owner/`
4. import registration modules from the app configuration or another explicit
   app-owned entrypoint
5. keep shared admin-site infrastructure in `core/adminsites/`

Do not place app-specific resources or admin classes in `core`.

## Tenant-Aware Apps

For owner-managed tenant data:

1. relate persistent domain rows to `TenantModel`
2. scope every owner-admin queryset to the active tenant
3. restrict relation and form-field choices to the active tenant
4. apply object-level tenant checks to view, change, and delete operations
5. gate sidebar visibility with the same access policy used by the target
   admin surface
6. use Django model permissions in addition to tenant membership
7. add a dedicated app policy only when the generic tenant access policy is
   insufficient

The owner-managed app contract is documented in
`docs/core/adminsites/owner-managed-apps.md`.

## Celery Tasks And Schedules

Celery autodiscovers installed-app `tasks` modules and `schedules` packages.

When the app needs background work:

1. keep thin task entrypoints in the owning app
2. keep orchestration and domain behavior in services
3. use serializable payloads rather than passing ORM objects
4. define retry behavior for the task's concrete failure modes
5. document idempotency expectations

When the app needs periodic work, keep its schedule definition in the app's
`schedules/` package. Do not add placeholder schedules for apps without a real
periodic workload.

## Translations

When stable owner-admin-facing copy is added:

1. mark the English source string for translation in code
2. run the repository translation extraction task
3. complete the Spanish catalog entry
4. compile and validate the catalog through the documented tasks

Translation work belongs to the same change as the stable source copy.

## Tests

Create tests under `<app>/tests/`, separated by layer where applicable.

Required behavior:

- inherit from the shared logged test bases
- keep external-service integration tests opt-in
- test tenant queryset, form-choice, permission, and object boundaries when
  the app is tenant-aware
- rely on unlabeled Django discovery so the complete suite finds the app

## Documentation

Mirror the app path under `docs/<app>/`.

At minimum:

1. document the app boundary and current responsibilities
2. link the app from `docs/project.md`
3. update `docs/capability-status.md` when the app changes implemented
   capability status
4. document optional runtime, environment, or external-service requirements

## Validation Checklist

Before closing the app integration:

- Django recognizes the app through `PROJECT_APPS`
- logging uses the project namespace
- admin registration is app-owned
- all tenant boundaries are covered where applicable
- tasks and schedules are discoverable only when implemented
- stable Spanish translations are complete
- the complete default test suite passes
- Ruff, typing scope, YAML, and Markdown gates remain green
