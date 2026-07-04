# Clone Readiness Procedure

This procedure verifies that a derived project can start from tracked files,
an empty database, and an empty local media directory.

Use disposable local infrastructure when exercising the destructive reset
steps. Do not reset a Compose project that contains data you need.

## Prepare A Clean Clone

1. Clone the repository into a new directory.
2. Create and activate a fresh virtual environment.
3. Install `requirements.txt`.
4. Copy `.env.example` to `.env`.
5. Replace the development secrets, database credentials, project name, and
   host ports when another local instance is already running.
6. Confirm `media/`, `staticfiles/`, and `minio-data/` contain no data copied
   from another project.

The README owns the exact platform-specific commands.

## Start From Empty Infrastructure

Use a unique Compose project name for the exercise. In VS Code, run:

1. `Docker: Validate Configuration`
2. `Docker: Start Infrastructure`
3. `Django: Migrate`
4. `Django: Create Superuser`
5. `Django: Check`
6. `Django: Test All`

The migration and superuser tasks are intentionally developer-run operations.
The default test suite creates its own test database and does not depend on
MinIO, MailHog, or Redis.

## Verify The Admin Surfaces

1. Start `Django: Run Server` from Run and Debug.
2. Sign in to `/admin/` with the new superuser.
3. Follow `docs/tenancy/setup.md` to create a neutral tenant, owner user, and
   primary owner membership.
4. Sign in to `/owner-admin/` with the owner user.
5. Confirm the expected tenant is active and the owner sees only sections
   allowed by their Django permissions.

## Verify Repository Cleanliness

After the exercise:

1. run `git status --short`
2. confirm no migration, catalog, compiled translation, media, collected
   static, or environment files were added unexpectedly
3. retain only intentional project customization

Local `.env`, database volumes, media, collected static files, and local
planning files must remain outside version control.

## Reset The Disposable Instance

Use `Docker: Remove Infrastructure And Volumes (Destructive)` only when the
selected Compose project is disposable. The MinIO bind-mounted
`minio-data/` directory is separate from named Compose volumes and must be
reviewed independently.
