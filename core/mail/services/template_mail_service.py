""" Project-level outbound templated mail service. """

from core.mail.composers import TemplateMailComposer
from core.mail.dtos import TemplateMailRequestDTO
from core.mail.services.mail_service import MailService


class TemplateMailService:
    """ Send outbound mail rendered from Django templates. """

    composer_class = TemplateMailComposer
    mail_service_class = MailService

    @classmethod
    def send(cls, request: TemplateMailRequestDTO, fail_silently: bool = False) -> int:
        """ Render one template pair and send the resulting outbound message.

        Args:
            request: Templated outbound mail request.
            fail_silently: Whether transport errors should be swallowed.

        Returns:
            int: Number of successfully delivered messages.
        """
        message = cls.composer_class.compose(request)
        return cls.mail_service_class.send(message, fail_silently=fail_silently)
