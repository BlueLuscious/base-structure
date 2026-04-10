""" Public mail service exports. """

from core.mail.dtos import MailAttachmentDTO, MailMessageDTO, MailRecipientDTO
from core.mail.mail_service import MailService
from core.mail.template_mail_service import TemplateMailService

__all__: list[str] = [
    "MailAttachmentDTO",
    "MailMessageDTO",
    "MailRecipientDTO",
    "MailService",
    "TemplateMailService",
]
