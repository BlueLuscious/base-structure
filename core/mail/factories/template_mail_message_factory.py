""" Factory that builds outbound mail DTOs from rendered templates. """

from collections.abc import Mapping, Sequence
from typing import Any
from core.mail.dtos import MailAttachmentDTO, MailMessageDTO, MailRecipientDTO
from core.mail.template_renderer import MailTemplateRenderer


class TemplateMailMessageFactory:
    """ Build outbound mail DTOs from template names and context. """

    renderer_class = MailTemplateRenderer

    @classmethod
    def build(
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
    ) -> MailMessageDTO:
        """ Build one outbound mail DTO from one template pair.

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

        Returns:
            MailMessageDTO: Rendered outbound mail payload.
        """
        text_body = cls.renderer_class.render_text(text_template_name, context)
        html_body = cls.renderer_class.render_html(html_template_name, context)

        return MailMessageDTO(
            subject=subject,
            to=to,
            text_body=text_body,
            html_body=html_body,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            headers=headers or {},
            attachments=attachments,
        )
