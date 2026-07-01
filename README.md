# Django Base

A reusable Django foundation for tenant-aware applications.

The required base provides:

- a custom user model and multitenancy foundation
- separate master and owner administration sites powered by Unfold
- English and Spanish administration
- tenant-aware media paths
- PostgreSQL and Redis-backed runtime foundations
- Celery Worker and Beat configuration
- synchronous and asynchronous template-based mail services
- Django Components and django-import-export integration

Included provider integrations add:

- local, WhiteNoise, Amazon S3, and Cloudflare R2 storage adapters
- MinIO for local S3-compatible development
- MailHog for local mail capture
- optional Discord repository notifications

These packages remain installed as part of the reusable base, while environment
configuration selects the active storage and delivery providers.

## Requirements

- Python 3.11 or newer
- Docker with Docker Compose
- GNU gettext when extracting or compiling translations

The Django process, Celery Worker, and Celery Beat run on the host. Docker
Compose provides development infrastructure only.

## Development Setup

1. Clone the repository and enter its directory.

   ```bash
   git clone <repository-url> django-base
   cd django-base
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```powershell
   .venv\Scripts\activate
   ```

   Unix or macOS:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and review its development values.

   Windows:

   ```powershell
   Copy-Item .env.example .env
   ```

   Unix or macOS:

   ```bash
   cp .env.example .env
   ```

5. Start the local infrastructure.

   ```bash
   docker compose up -d
   ```

6. Apply migrations and create a superuser.

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Start Django.

   ```bash
   python manage.py runserver
   ```

The technical administration site is available at `/admin/` and requires an
active superuser.

The tenant-aware owner administration site is available at `/owner-admin/`.
Its minimum setup is:

1. create an active tenant from the technical admin
2. create an active staff user
3. create an active owner membership linking that user to the tenant
4. mark the membership as primary when it should be the automatic fallback

Additional Django permissions control access to owner-managed account sections.

## Local Services

Default endpoints from `.env.example`:

- PostgreSQL: `127.0.0.1:5432`
- MinIO API: `http://127.0.0.1:9000`
- MinIO console: `http://127.0.0.1:9001`
- MailHog SMTP: `127.0.0.1:1025`
- MailHog web UI: `http://127.0.0.1:8025`
- Redis: `127.0.0.1:6379`

Host ports are configurable, allowing independently named clones to use
different ports when they run simultaneously.

Compose generates container, network, and volume names from each project name
instead of using global fixed container names. Service discovery inside each
Compose network still uses the stable service names `db`, `minio`, `mailhog`,
and `redis`.

Stop services without removing their data:

```bash
docker compose stop
```

Remove containers and networks while retaining the PostgreSQL volume:

```bash
docker compose down
```

Reset the named PostgreSQL volume only when losing local database data is
acceptable:

```bash
docker compose down -v
```

The `minio-data/` bind-mounted directory is independent from named Compose
volumes and is not removed by `docker compose down -v`.

## Celery

Start a worker after Redis is available.

Windows:

```powershell
.venv\Scripts\celery.exe -A core.celery worker --loglevel=info --pool=solo
```

Unix or macOS:

```bash
.venv/bin/celery -A core.celery worker --loglevel=info
```

Start Beat in a separate terminal:

```bash
celery -A core.celery beat --loglevel=info
```

Beat enqueues scheduled work; a running worker executes it.

## Documentation

Start with [docs/project.md](docs/project.md). Detailed documentation covers:

- accounts and authentication
- tenant persistence, access, and runtime resolution
- master and owner administration sites
- storage providers and integration testing
- Celery and scheduled tasks
- mail composition, templates, and runtime behavior
- logging and reusable form infrastructure
- optional Discord repository notifications

Ready-to-copy storage environment combinations live under
`docs/env-examples/`.

Environment example names use:

```text
.env.<media-provider>.<static-provider>.example
```

Available combinations are:

- local media with local static files
- S3 media with local, S3, or WhiteNoise static files
- R2 media with local, R2, or WhiteNoise static files

Discord notification setup and lifecycle behavior are documented in
[docs/github/workflows/discord.md](docs/github/workflows/discord.md).

## Starting A New Project

Before using a clone as a new project:

- update repository metadata, Git remotes, and stable display branding
- replace secrets and configure allowed hosts and trusted origins
- choose project-specific database credentials and keep the schema, Compose,
  and Django settings aligned
- select the media and static storage providers
- configure mail delivery, Redis, Celery, language, and timezone
- create the initial superuser, tenant, owner membership, and permissions
- retain, reconfigure, or remove the optional Discord workflow
- review existing migrations before adding project-specific models
- run Django checks, the complete default test suite, translation checks, and
  production deployment checks

## Translations

English is the default language and Spanish is the supported alternative.
Owner-admin-facing copy must be marked for translation when introduced, and
stable Spanish translations must be completed in the same change.

Windows users can download the required GNU gettext tools from:

- [Gettext for Windows](https://github.com/mlocati/gettext-iconv-windows/releases/tag/v1.0-v1.18-r3)

```bash
python manage.py makemessages -l es --ignore .venv --ignore node_modules --ignore '*.txt'
python manage.py compilemessages -l es
```

## Production

The included environment values and Compose services are for local development.
Before deployment, replace all secrets and credentials and review Django's
deployment checklist, HTTPS, trusted origins, cookies, storage, mail delivery,
logging, backups, and worker operations.

See Django's
[deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
and run deployment checks with production-like settings before release.
