# Capability Removal Guide

This guide defines how a derived project can remove an unused base capability
without leaving imports, settings, routes, tests, or documentation behind.

Removing a capability is a contract change. Review the complete dependency
chain before deleting its package or requirement.

## Inventory The Capability

Search the complete repository for:

- Python imports and package initialization
- `INSTALLED_APPS` and `PROJECT_APPS`
- middleware
- URL includes and named routes
- template loaders, built-ins, context processors, and static finders
- storage aliases and adapters
- Celery task or schedule discovery
- environment variables and examples
- Docker Compose services, health checks, volumes, and ports
- tests, fixtures, and opt-in integration flags
- documentation and capability-status entries
- runtime and development requirement sources

Generated lock files are outputs. Change the reviewed requirement source
first, then regenerate the affected lock through the documented dependency
task.

## Remove Runtime Wiring

Remove the capability from every runtime entrypoint it owns:

1. settings and installed apps
2. URLs
3. middleware
4. templates and static-file wiring
5. storage, mail, Celery, or admin adapters
6. app configuration and explicit registration imports

Do not leave compatibility branches for a capability that the derived project
has intentionally removed.

## Remove Infrastructure And Environment Configuration

When the capability owns local infrastructure:

1. remove its Compose service and dependencies
2. remove unused ports, volumes, health checks, and bootstrap containers
3. remove its variables from `.env.example` and shared environment examples
4. update VS Code tasks that operate the service

Do not remove shared infrastructure merely because one consumer was removed.
For example, Redis may still support Celery after a result consumer changes.

## Remove Dependencies

1. remove direct packages from `requirements.in` or
   `requirements-dev.in`
2. regenerate the corresponding pinned lock
3. run dependency consistency and security checks
4. verify no transitive package is being treated as a direct API elsewhere

## Remove Tests And Documentation

Delete tests only when their production contract no longer exists. Preserve
shared infrastructure coverage used by remaining capabilities.

Update:

- the owning package documentation
- `docs/project.md`
- `docs/capability-status.md`
- README setup steps when first-run behavior changes
- CI, VS Code, and environment documentation when commands change

## Final Verification

After removal:

1. search again for the package, setting, environment variable, URL, and
   service names
2. run Django checks
3. run the complete default test suite
4. run formatting, linting, typing, YAML, Markdown, and dependency gates
5. render Docker Compose configuration when infrastructure changed
6. confirm the documented clean-clone path still works

Migration generation and translation extraction remain explicit
developer-run operations under the repository workflow.
