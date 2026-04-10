""" Public mail service exports. """

from core.mail.dtos import MailAttachmentDTO, MailMessageDTO, MailRecipientDTO
from core.mail.mail_service import MailService

__all__: list[str] = [
    "MailAttachmentDTO",
    "MailMessageDTO",
    "MailRecipientDTO",
    "MailService",
]
