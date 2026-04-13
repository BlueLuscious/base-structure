""" Project-level outbound mail service. """

from collections.abc import Sequence
from core.mail.backends import DjangoMailDeliveryBackend
from core.mail.dtos import MailMessageDTO


class MailService:
    """ Send outbound mail through the project's current delivery backend. """

    delivery_backend_class = DjangoMailDeliveryBackend

    @classmethod
    def send(cls, message: MailMessageDTO, fail_silently: bool = False) -> int:
        """ Send one outbound message.

        Args:
            message: Outbound mail payload.
            fail_silently: Whether transport errors should be swallowed.

        Returns:
            int: Number of successfully delivered messages.
        """
        return cls.delivery_backend_class.send(message, fail_silently=fail_silently)

    @classmethod
    def send_many(cls, messages: Sequence[MailMessageDTO], fail_silently: bool = False) -> int:
        """ Send multiple outbound messages.

        Args:
            messages: Outbound mail payloads.
            fail_silently: Whether transport errors should be swallowed.

        Returns:
            int: Number of successfully delivered messages.
        """
        return cls.delivery_backend_class.send_many(messages, fail_silently=fail_silently)
