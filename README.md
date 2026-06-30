# Django Base

A reusable Django foundation for tenant-aware applications.

The project provides:

- a custom user model and multitenancy foundation
- separate master and owner administration sites powered by Unfold
- English and Spanish administration
- local, WhiteNoise, Amazon S3, and Cloudflare R2 storage adapters
- tenant-aware media paths
- PostgreSQL, MinIO, MailHog, and Redis development infrastructure
- Celery Worker and Beat configuration
- synchronous and asynchronous template-based mail services
- Django Components and django-import-export integration points

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

The technical administration site is available at `/admin/`. The tenant-aware
owner administration site is available at `/owner-admin/`. Create the initial
tenant, membership, and owner access manually through the administration
interfaces.

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

Ready-to-copy storage environment combinations live under
`docs/env-examples/`.

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
