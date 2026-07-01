# Mail Composers

This document explains how the project should use mail composers under `core/mail/composers/`.

See also:

- `docs/core/mail/mail.md`
- `docs/tenancy/tenancy.md`

## Goal

Composers exist to assemble one outbound mail payload before the transport layer sends it.

They should:

- accept one higher-level input
- resolve the context needed for that mail flow
- apply mail policies such as sender and reply rules
- build one `MailMessageDTO`
- avoid performing the actual delivery

## Current Composer

The current project-wide composer is:

- `TemplateMailComposer`

It accepts one `TemplateMailRequestDTO` and returns one `MailMessageDTO`.

Its current responsibilities are:

- resolve the effective sender through `SystemMailSenderPolicy`
- bind one explicit tenant when the request carries one
- delegate HTML and plain-text rendering through the existing template factory
- return one transport-ready message DTO

## Rule Of Thumb

Keep this split:

- composers assemble mail payloads
- services send mail payloads
- policies decide sender and reply behavior
- resolvers gather tenant-aware or domain-aware data

This means:

- `MailService` remains the single source of truth for delivery
- composers remain the source of truth for mail assembly

## When To Use `TemplateMailComposer` Directly

Use `TemplateMailComposer` directly when:

- the flow is still generic
- the caller already has the final subject, recipients, templates, and context
- the mail does not yet deserve its own domain-specific abstraction

Typical examples:

- one generic admin notification
- one manual smoke-test flow
- one temporary project-wide message not owned by a single app yet

Example:

```python
from core.mail import MailService, TemplateMailComposer, TemplateMailRequestDTO

request = TemplateMailRequestDTO(
    subject="Example notification",
    to=[...],
    context={
        "mail_title": "Example notification",
        "mail_body": "This message was composed directly.",
    },
    html_template_name="core/mail/messages/test_message.html",
    text_template_name="core/mail/messages/test_message.txt",
)

message = TemplateMailComposer.compose(request)
MailService.send(message)
```

## When To Create A Domain Composer

Create a domain composer when:

- the mail belongs clearly to one business flow
- recipient selection stops being generic
- reply behavior depends on the business case
- the subject and template context should no longer be assembled ad hoc in views or services

Typical examples:

- customer request notifications
- customer confirmation emails
- account recovery or invitation flows owned by one app

## Composer Design Rules

When creating a new composer:

1. keep one primary composer class per file
2. accept one domain input or one explicit DTO instead of many loose parameters
3. resolve recipients through policies or resolvers when possible
4. resolve `reply_to` through policy helpers instead of hardcoding it inline
5. return one `MailMessageDTO`
6. do not send the message directly from the composer

## Example Future Composer

One hypothetical app-owned composer for a customer request could look like this:

```python
from core.mail import (
    MailMessageDTO,
    TemplateMailComposer,
    TemplateMailRequestDTO,
    TenantMailRecipientResolver,
    TenantMailReplyPolicy,
)
from example_app.dtos import CustomerRequestDTO


class CustomerRequestMailComposer:
    """ Compose one tenant notification for a customer request. """

    @classmethod
    def compose(cls, request_dto: CustomerRequestDTO) -> MailMessageDTO:
        """ Build one outbound mail payload for a customer request.

        Args:
            request_dto: App-owned DTO carrying the customer request.

        Returns:
            MailMessageDTO: Transport-ready outbound message.
        """
        tenant_recipient = TenantMailRecipientResolver.resolve_contact_recipient(
            request_dto.tenant
        )
        if tenant_recipient is None:
            raise ValueError("Customer request mail requires one tenant contact recipient.")

        request = TemplateMailRequestDTO(
            subject=f"New customer request from {request_dto.customer_name}",
            to=[tenant_recipient],
            context={
                "mail_title": "New customer request",
                "mail_intro": "A customer submitted a new request.",
                "mail_body": request_dto.message,
                "customer_name": request_dto.customer_name,
                "customer_email": request_dto.customer_email,
            },
            html_template_name="example_app/mail/customer_request.html",
            text_template_name="example_app/mail/customer_request.txt",
            tenant=request_dto.tenant,
            reply_to=TenantMailReplyPolicy.resolve_customer_reply_to(
                request_dto.customer_email
            ),
        )
        return TemplateMailComposer.compose(request)
```

## How That Composer Would Be Used

The application flow should stay simple:

```python
from core.mail import MailService

message = CustomerRequestMailComposer.compose(request_dto)
MailService.send(message)
```

If one app wants a thin app-owned sender facade, it can wrap that:

```python
class CustomerRequestMailService:
    """ Send customer request emails for the owning app. """

    @classmethod
    def send(cls, request_dto: CustomerRequestDTO) -> int:
        """ Compose and send one customer request mail.

        Args:
            request_dto: App-owned DTO carrying the customer request.

        Returns:
            int: Number of successfully delivered messages.
        """
        message = CustomerRequestMailComposer.compose(request_dto)
        return MailService.send(message)
```

## Ownership Rule

Keep project-wide generic composers in `core/mail/composers/`.

If a composer becomes clearly owned by one app or one business flow, prefer moving it into that app instead of growing `core/` with domain behavior.
