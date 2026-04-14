# Core Mail

This document explains the project-wide outbound mail service under `core/mail/`.

See also:

- `docs/project.md`
- `docs/core/core.md`
- `docs/core/mail/composers/composers.md`

## Goal

`core/mail/` exists to provide one reusable outbound mail boundary for the whole project.

It should:

- keep mail delivery out of domain apps
- expose one stable service contract
- build on top of Django's native mail stack
- stay ready for future asynchronous delivery without changing caller code

## Current Structure

Current contents:

- `dtos/`
- `backends/`
- `composers/`
- `factories/`
- `renderers/`
- `resolvers/`
- `serializers/`
- `policies/`
- `services/`

## Current Runtime Direction

The current mail implementation is intentionally:

- synchronous
- based on `django.core.mail`
- built on top of `EmailMultiAlternatives`
- able to build outbound messages either from raw DTO bodies or from Django templates
- already wired for asynchronous dispatch through the project-wide Celery runtime

This keeps the first runtime simple while preserving a clear boundary for future async delivery.

## Responsibilities

### `MailService`

`MailService` is the project entrypoint for outbound mail.

Current responsibilities:

- send one mail message
- send multiple mail messages
- enqueue one mail message for asynchronous delivery
- delegate actual delivery to the configured project backend
- log meaningful delivery and enqueue boundaries without logging full message bodies

### `TemplateMailComposer`

`TemplateMailComposer` is the composition entrypoint for templated outbound mail.

Current responsibilities:

- accept one `TemplateMailRequestDTO`
- resolve sender policy
- bind one explicit tenant context when needed
- render one plain-text and one HTML template
- build one `MailMessageDTO`

It does not send mail.

For composer usage and design rules, see:

- `docs/core/mail/composers/composers.md`

### `TemplateMailService`

`TemplateMailService` is the higher-level entrypoint for templated outbound mail.

Current responsibilities:

- accept one `TemplateMailRequestDTO`
- delegate mail composition to `TemplateMailComposer`
- enqueue one templated mail request for asynchronous delivery
- delegate final delivery to `MailService`
- log meaningful templated delivery and enqueue boundaries without duplicating low-level renderer details

### DTOs

The DTO layer exists so the service contract stays explicit and easy to evolve.

Current DTOs:

- `MailRecipientDTO`
- `MailAttachmentDTO`
- `MailMessageDTO`
- `TemplateMailRequestDTO`

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
- one `TemplateMailRequestDTO` into one `MailMessageDTO`

### `serializers/`

This package owns conversion between mail DTOs and Celery-safe payload dictionaries.

Current serializers:

- `MailMessagePayloadSerializer`
- `TemplateMailRequestPayloadSerializer`

They convert:

- one `MailMessageDTO` into one plain async payload and back
- one `TemplateMailRequestDTO` into one plain async payload and back

### `renderers/`

This package owns mail template rendering.

Current renderer:

- `MailTemplateRenderer`

It renders the HTML and plain-text mail templates after merging the tenant-aware base context.

### `resolvers/`

This package owns mail data lookups and assembly helpers.

Current resolvers:

- `MailTemplateBaseContextBuilder`
- `TenantMailContextResolver`
- `TenantMailRecipientResolver`

They gather:

- the effective base template context shared by synchronous rendering and asynchronous templated snapshotting
- tenant-aware template context values
- preferred tenant contact recipients

### `policies/`

This package owns outbound mail behavior decisions.

Current policies:

- `SystemMailSenderPolicy`
- `TenantMailReplyPolicy`

They decide:

- which technical sender override should be used when one exists
- which reply target fits one business flow

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
- resolve tenant-aware branding and contact values from the active tenant context when one exists
- keep branding values optional when no active tenant context exists
- allow future template override by template name
- avoid full layout replacement as the default extension path

Current tenant-aware behavior:

- `product_name` resolves from tenant branding display data first, then the tenant business name
- `support_email` resolves from tenant operational contact data on `TenantModel`, with business email as a fallback
- `phone_number` and `website_url` resolve from tenant operational contact data on `TenantModel`
- `TemplateMailService` may use either the active runtime tenant context or one explicit tenant passed by the caller
- when neither value exists, templates should degrade to a neutral layout instead of inventing unrelated branding

### Shared async task entrypoints

Mail async entrypoints now live under the shared Celery task layer in:

Current mail tasks:

- `core/tasks/mail/tasks.py`
- `send_mail_message_task`
- `send_templated_mail_task`

Current task logging direction:

- log task execution boundaries with compact operational context
- let the task and service layers log different boundaries instead of duplicating the same full event narrative

Current retry direction for both tasks:

- retry transient transport failures only
- current retryable errors:
  - `SMTPException`
  - `TimeoutError`
  - `ConnectionError`
- current retry policy:
  - `max_retries=3`
  - exponential backoff enabled
  - jitter enabled

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

Current meaning of `DEFAULT_FROM_EMAIL`:

- it is the project-level fallback sender used when one outbound message does not provide an explicit `from_email`
- it is appropriate for system-originated mail
- it is not the final tenant-owned sender identity for future business mail sent on behalf of one tenant
- future tenant-specific sender rules should stay separate from simple tenant contact metadata

## Sender And Reply Policy

The current project should treat outbound mail identity in three separate layers:

1. technical sender
2. tenant contact channel
3. reply target

### Technical Sender

Current rule:

- `DEFAULT_FROM_EMAIL` is the system-level sender fallback
- it should be used for system-originated mail
- it should also be used for tenant-aware mail until a future tenant-specific verified sender flow exists

Current non-goal:

- do not treat `TenantModel.business_email` or `TenantModel.support_email` as the real authenticated SMTP sender
- do not set the customer's email address as `from_email`

Using an unverified tenant email or customer email as the real sender would blur technical sender identity and likely create deliverability problems.

### Tenant Contact Channel

Current rule:

- `support_email` is the preferred tenant contact channel
- `business_email` is the fallback tenant contact channel

These values represent business contact metadata, not the technical mail sender.

### Reply Target

Current rule:

- use `reply_to` to represent who should receive replies
- do not overload `from_email` to fake user or tenant identity

Recommended patterns:

- system mail:
  - `from_email = DEFAULT_FROM_EMAIL`
  - `reply_to = []` unless the system flow needs a specific reply target
- tenant notification mail sent to tenant staff:
  - `from_email = DEFAULT_FROM_EMAIL`
  - `to = tenant.support_email or tenant.business_email`
- customer-originated request forwarded to tenant staff:
  - `from_email = DEFAULT_FROM_EMAIL`
  - `reply_to = [customer_email]`
  - `to = tenant.support_email or tenant.business_email`
- future customer-facing tenant-aware mail:
  - `from_email = DEFAULT_FROM_EMAIL`
  - `reply_to = [tenant.support_email or tenant.business_email]` when a business reply channel should be exposed

This keeps the technical sender under project control while still allowing the correct human reply path.

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
- `RUN_ASYNC_MAIL_INTEGRATION_TESTS=True` for the asynchronous worker-backed suite
- optional override: `MAILHOG_MESSAGES_API_URL=http://127.0.0.1:8025/api/v2/messages`
- optional override: `MAILHOG_WAIT_TIMEOUT_SECONDS=20`
- optional override: `MAILHOG_POLL_INTERVAL_SECONDS=0.25`

Current integration coverage verifies:

- sending one real message to MailHog
- sending multiple real messages to MailHog
- sending one real templated message to MailHog
- sending multiple real templated messages to MailHog
- sending one real tenant-aware templated message to MailHog
- sending multiple real tenant-aware templated messages to MailHog
- sending one real raw mail message through Celery to MailHog
- sending one real templated mail message through Celery to MailHog
- sending one real tenant-aware templated mail message through Celery to MailHog

The integration suite inspects MailHog through its HTTP API after the SMTP delivery succeeds.

The asynchronous integration subset additionally expects:

- Redis to be available
- one Celery worker to be running
- `CELERY_TASK_ALWAYS_EAGER=False`
- on Windows local development, the worker should use `--pool=solo`

Example command:

```powershell
$env:RUN_MAIL_INTEGRATION_TESTS='True'
.\.venv\Scripts\python.exe manage.py test core.tests.mail.integration
```

Asynchronous example command:

```powershell
$env:RUN_MAIL_INTEGRATION_TESTS='True'
$env:RUN_ASYNC_MAIL_INTEGRATION_TESTS='True'
.\.venv\Scripts\python.exe manage.py test core.tests.mail.integration.test_mailhog_async_mail_service_integration core.tests.mail.integration.test_mailhog_async_template_mail_service_integration
```

## Async Direction

The current mail stack now supports explicit asynchronous dispatch through the project-wide Celery runtime.

Current direction:

- keep `MailService` as the caller-facing contract for raw mail
- keep `TemplateMailService` as the caller-facing contract for templated mail
- serialize DTOs into plain Celery-safe payloads before enqueueing
- snapshot templated mail context during enqueue through the same shared base-context builder used by synchronous rendering
- rebuild DTOs inside thin Celery tasks before delegating back to the synchronous services

Additional future direction:

- keep the tenant-aware mail context resolver reusable when async delivery grows later
- keep technical sender configuration separate from simple contact metadata until verified outbound sender rules are defined
- add domain-specific async mail flows on top of the existing shared mail tasks and services when real business flows appear

## Refinement Direction

The current structure is good enough for the base runtime, but the next refinement should keep mail policy responsibilities explicit.

Suggested responsibilities:

- `TenantMailContextResolver`
  - branding and contact context for templates
- `TenantMailRecipientResolver`
  - resolve the preferred tenant-facing `to` address
- `TenantMailReplyPolicy`
  - resolve the correct `reply_to` target for one business flow
- future `TenantMailSenderPolicy`
  - decide whether one flow should use the system sender fallback or a future verified tenant sender

The rule of thumb should be:

- resolvers gather data
- policies decide outbound mail behavior
- composers assemble already-decided payloads
- services send already-decided payloads

That split keeps the mail stack composable once customer-facing and async flows begin to grow.

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
