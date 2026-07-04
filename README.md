# Django Base

A reusable Django foundation for tenant-aware applications. It includes a
custom user model, tenant-aware master and owner admin sites powered by Unfold,
Celery, synchronous and asynchronous mail, configurable storage, Django
Components, and django-import-export.

Docker Compose provides PostgreSQL, MinIO, MailHog, and Redis for local
development. Django, Celery Worker, and Celery Beat run on the host.

## Requirements

- Python 3.11 or newer
- Docker with Docker Compose
- GNU gettext when extracting or compiling translations

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

   `requirements.in` owns the reviewed direct dependencies.
   `requirements.txt` is the generated, fully pinned runtime lock.

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
active superuser. The tenant-aware owner administration site is available at
`/owner-admin/`.

See the
[initial tenant setup](docs/tenancy/setup.md)
for initial tenant and owner access. Use the
[clone-readiness procedure](docs/clone-readiness.md)
when validating a derived project from empty local state.

## Documentation

Start with:

- [project structure and documentation map](docs/project.md)
- [clean-clone verification](docs/clone-readiness.md)
- [capability status](docs/capability-status.md)
- [project configuration](docs/core/config/config.md)
- [Celery runtime](docs/core/celery/celery.md)
- [storage providers and environment examples](docs/core/config/storage/storage.md)
- [Discord notifications](docs/github/workflows/discord.md)

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

Development defaults are not production-safe. Replace credentials and review
Django's
[deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
before release.

Run Django's deployment checks with production-intended environment values:

```bash
python manage.py check --deploy
```
