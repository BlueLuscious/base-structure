""" Public resolver exports for the mail package. """

from core.mail.resolvers.tenant_mail_context_resolver import TenantMailContextResolver
from core.mail.resolvers.tenant_mail_recipient_resolver import TenantMailRecipientResolver

__all__: list[str] = [
    "TenantMailContextResolver",
    "TenantMailRecipientResolver",
]
