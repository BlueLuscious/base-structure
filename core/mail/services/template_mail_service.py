""" Project-level outbound templated mail service. """

from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator
from core.mail.dtos import TemplateMailRequestDTO
from core.mail.factories import TemplateMailMessageFactory
from core.mail.policies import SystemMailSenderPolicy
from core.mail.services.mail_service import MailService
from tenancy.runtime import ActiveTenantContext

if TYPE_CHECKING:
    from tenancy.models import TenantModel


class TemplateMailService:
    """ Send outbound mail rendered from Django templates. """

    message_factory_class = TemplateMailMessageFactory
    mail_service_class = MailService
    tenant_context_class = ActiveTenantContext
    sender_policy_class = SystemMailSenderPolicy

    @classmethod
    def send(cls, request: TemplateMailRequestDTO, fail_silently: bool = False) -> int:
        """ Render one template pair and send the resulting outbound message.

        Args:
            request: Templated outbound mail request.
            fail_silently: Whether transport errors should be swallowed.

        Returns:
            int: Number of successfully delivered messages.
        """
        resolved_from_email = cls.sender_policy_class.resolve(
            explicit_from_email=request.from_email,
            tenant=request.tenant,
        )

        with cls._use_tenant_context(request.tenant):
            message = cls.message_factory_class.build(
                request=request,
                from_email=resolved_from_email,
            )
        return cls.mail_service_class.send(message, fail_silently=fail_silently)

    @classmethod
    @contextmanager
    def _use_tenant_context(cls, tenant: "TenantModel | None") -> Iterator[None]:
        """ Temporarily bind one explicit tenant to the current mail rendering flow.

        Args:
            tenant: Tenant to bind while the mail payload is rendered.

        Yields:
            Iterator[None]: Empty context manager body.
        """
        if tenant is None:
            yield
            return

        tenant_token = cls.tenant_context_class.set(tenant)

        try:
            yield
        finally:
            cls.tenant_context_class.reset(tenant_token)
