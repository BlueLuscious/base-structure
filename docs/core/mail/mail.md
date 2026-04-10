# Core Mail

This document explains the project-wide outbound mail service under `core/mail/`.

See also:

- `docs/project.md`
- `docs/core/core.md`

## Goal

`core/mail/` exists to provide one reusable outbound mail boundary for the whole project.

It should:

- keep mail delivery out of domain apps
- expose one stable service contract
- build on top of Django's native mail stack
- stay ready for future asynchronous delivery without changing caller code

## Current Structure

Current contents:

- `mail_service.py`
- `template_mail_service.py`
- `template_renderer.py`
- `dtos/`
- `backends/`
- `factories/`
- `tasks/`

## Current Runtime Direction

The current mail implementation is intentionally:

- synchronous
- based on `django.core.mail`
- built on top of `EmailMultiAlternatives`
- able to build outbound messages either from raw DTO bodies or from Django templates

This keeps the first runtime simple while preserving a clear boundary for future async delivery.

## Responsibilities

### `MailService`

`MailService` is the project entrypoint for outbound mail.

Current responsibilities:

- send one mail message
- send multiple mail messages
- delegate actual delivery to the configured project backend

### `TemplateMailService`

`TemplateMailService` is the higher-level entrypoint for templated outbound mail.

Current responsibilities:

- render one plain-text and one HTML template
- build one `MailMessageDTO`
- delegate final delivery to `MailService`

### DTOs

The DTO layer exists so the service contract stays explicit and easy to evolve.

Current DTOs:

- `MailRecipientDTO`
- `MailAttachmentDTO`
- `MailMessageDTO`

This keeps mail payload assembly separate from Django's concrete message object.

### `backends/`

This package owns delivery implementations.

Current backend:

- `DjangoMailDeliveryBackend`

It sends mail through Django's configured email backend.

### `factories/`

This package owns translation from project DTOs into framework objects.

Current factory:

- `EmailMultiAlternativesFactory`
- `TemplateMailMessageFactory`

They convert:

- one `MailMessageDTO` into one Django `EmailMultiAlternatives` instance
- one template pair plus context into one `MailMessageDTO`

## Templates

Mail templates now live under:

- `core/templates/mail/layouts/`
- `core/templates/mail/partials/`
- `core/templates/mail/messages/`

Current structure:

- one reusable HTML base layout
- one reusable plain-text base layout
- one mandatory footer partial in both formats
- one reusable CTA button partial for HTML mails
- one generic example message template pair

The current layout direction is:

- always render plain text and HTML together
- keep the system footer structure mandatory
- keep branding values optional until tenant-aware mail context is resolved
- allow future template override by template name
- avoid full layout replacement as the default extension path

### `tasks/`

This package is intentionally reserved for future async delivery.

It is not active yet.

## Current Settings Direction

The current project mail service uses the standard Django email settings from `core/settings.py`.

Current examples:

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`

For local development, the defaults target MailHog through SMTP.

Recommended local MailHog values:

- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST=127.0.0.1`
- `EMAIL_PORT=1025`
- `EMAIL_HOST_USER=`
- `EMAIL_HOST_PASSWORD=`
- `EMAIL_USE_TLS=False`
- `EMAIL_USE_SSL=False`
- `DEFAULT_FROM_EMAIL=noreply@localhost`

## Local Manual Smoke Test

One simple way to validate the runtime mail flow manually is:

1. start Docker services so MailHog is available
2. keep the local mail settings pointed at MailHog
3. send one message through `MailService`
4. confirm the message appears in the MailHog web UI

MailHog endpoints in local development:

- SMTP: `127.0.0.1:1025`
- Web UI: `http://127.0.0.1:8025`

## Tests

The mail package now follows the same split already used by storage:

- `core/tests/mail/unit/`
- `core/tests/mail/integration/`

### Unit Tests

Unit tests verify:

- DTO normalization
- `EmailMultiAlternatives` factory behavior
- synchronous delivery through Django's local memory backend
- template rendering
- template-based message DTO creation
- templated delivery through the local memory backend

### Integration Tests

Mail integration tests are opt-in and target MailHog through real SMTP delivery.

Enable them with:

- `RUN_MAIL_INTEGRATION_TESTS=True`
- optional override: `MAILHOG_MESSAGES_API_URL=http://127.0.0.1:8025/api/v2/messages`

Current integration coverage verifies:

- sending one real message to MailHog
- sending multiple real messages to MailHog
- sending one real templated message to MailHog
- sending multiple real templated messages to MailHog

The integration suite inspects MailHog through its HTTP API after the SMTP delivery succeeds.

Example command:

```powershell
$env:RUN_MAIL_INTEGRATION_TESTS='True'
.\.venv\Scripts\python.exe manage.py test core.tests.mail.integration
```

## Future Direction

The service boundary is intentionally prepared for future asynchronous delivery.

Current expected next step:

- keep `MailService` as the caller-facing contract
- add async task execution under `core/mail/tasks/`
- keep synchronous payload building and framework integration inside the existing DTO, backend, and factory layers

The project already expects Celery plus Redis to become the async stack when async delivery is wired.

## What Should Live Here

Good candidates:

- project-wide mail DTOs
- project-wide mail delivery services
- framework-specific mail factories
- async task entrypoints for outbound mail

## What Should Not Live Here

Avoid placing these here:

- domain-specific email business rules
- email template content that belongs to one app only
- domain orchestration for account flows, tenancy flows, or future domain apps

Those concerns should stay in the app that decides when a mail should be sent.
