""" Project-level outbound templated mail service. """

from collections.abc import Mapping, Sequence
from typing import Any
from core.mail.dtos import MailAttachmentDTO, MailRecipientDTO
from core.mail.factories import TemplateMailMessageFactory
from core.mail.mail_service import MailService


class TemplateMailService:
    """ Send outbound mail rendered from Django templates. """

    message_factory_class = TemplateMailMessageFactory
    mail_service_class = MailService

    @classmethod
    def send(
        cls,
        *,
        subject: str,
        to: Sequence[MailRecipientDTO],
        context: Mapping[str, Any],
        html_template_name: str,
        text_template_name: str,
        from_email: str | None = None,
        cc: Sequence[MailRecipientDTO] = (),
        bcc: Sequence[MailRecipientDTO] = (),
        reply_to: Sequence[str] = (),
        headers: Mapping[str, str] | None = None,
        attachments: Sequence[MailAttachmentDTO] = (),
        fail_silently: bool = False,
    ) -> int:
        """ Render one template pair and send the resulting outbound message.

        Args:
            subject: Mail subject line.
            to: Primary recipients.
            context: Template context values.
            html_template_name: HTML template path.
            text_template_name: Plain-text template path.
            from_email: Optional sender override.
            cc: Optional carbon-copy recipients.
            bcc: Optional blind carbon-copy recipients.
            reply_to: Optional reply-to addresses.
            headers: Optional custom headers.
            attachments: Optional outbound attachments.
            fail_silently: Whether transport errors should be swallowed.

        Returns:
            int: Number of successfully delivered messages.
        """
        message = cls.message_factory_class.build(
            subject=subject,
            to=to,
            context=context,
            html_template_name=html_template_name,
            text_template_name=text_template_name,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            headers=headers,
            attachments=attachments,
        )
        return cls.mail_service_class.send(message, fail_silently=fail_silently)
