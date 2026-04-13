""" Public mail package exports. """

from core.mail.dtos import MailAttachmentDTO, MailMessageDTO, MailRecipientDTO, TemplateMailRequestDTO
from core.mail.policies import SystemMailSenderPolicy, TenantMailReplyPolicy
from core.mail.resolvers import TenantMailContextResolver, TenantMailRecipientResolver
from core.mail.services import MailService, TemplateMailService

__all__: list[str] = [
    "MailAttachmentDTO",
    "MailMessageDTO",
    "MailRecipientDTO",
    "TemplateMailRequestDTO",
    "MailService",
    "SystemMailSenderPolicy",
    "TenantMailContextResolver",
    "TenantMailRecipientResolver",
    "TenantMailReplyPolicy",
    "TemplateMailService",
]
