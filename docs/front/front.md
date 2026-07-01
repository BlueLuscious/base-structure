# Front App

This document defines the intended future role of `front/` and the process for
wiring public frontend surfaces.

See also:

- `docs/project.md`
- `docs/capability-status.md`
- `docs/tenancy/tenancy.md`
- `docs/tenancy/runtime.md`
- `docs/tenancy/resolution.md`

## Current Status

`front/` is a designed future integration surface. It is not present in the
current repository tree and is not registered in `core/settings.py`.

When introduced, it is intended to own:

- reusable UI components
- public pages and templates
- public base views and view mixins
- page-specific CSS and JavaScript
- frontend route definitions
- sandbox examples for reusable components

It must remain decoupled from owner-admin concerns and should become
tenant-aware only when a real frontend flow requires tenant context.

## Future Frontend Surface Types

The frontend may contain more than one explicit surface:

- tenant-aware routes whose URL identifies the tenant
- global routes without tenant context
- public or anonymous routes that do not require membership
- authenticated tenant routes with tenant-scoped access policies

One surface must not silently inherit the rules of another.

## Future Tenant-Aware Frontend By Path

When the first tenant-aware frontend flow appears, the preferred direction is
path-based tenant identity.

Example route contract:

```text
/t/<tenant-slug>/<resource>/
```

Recommended process:

1. define one stable path convention
2. resolve tenant identity before page-specific business logic
3. keep tenant resolution separate from access policy
4. validate membership or public visibility after resolution
5. scope app-owned queries to the resolved tenant
6. preserve the tenant path in generated links
7. keep reusable components independent from tenant resolution

`PathTenantResolutionStrategy` is the existing extension hook for this future
flow. It is deliberately inactive today.

## Future Global Frontend Pages

When a page is not tenant-aware:

- do not force an active tenant into its route
- do not depend on tenant-scoped query helpers
- do not import tenant access policies
- introduce tenant context only through an explicit transition

Possible examples include landing, sign-in, documentation, or support pages.

## Implementation Gate

Before creating `front/`:

1. identify the first real page and its access contract
2. define explicit component, view, template, asset, sandbox, and test ownership
3. register the app and routes explicitly
4. activate only the tenant-resolution strategies required by real routes
5. add component sandbox examples when reusable components are introduced
6. add rendering, contract, and integration tests
7. update `docs/project.md` and `docs/capability-status.md`

Do not create placeholder business pages or claim frontend runtime capability
before the corresponding code exists.
