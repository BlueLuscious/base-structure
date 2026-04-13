""" Project-level outbound mail service. """

from collections.abc import Sequence
from celery.result import AsyncResult
from core.mail.backends import DjangoMailDeliveryBackend
from core.mail.dtos import MailMessageDTO
from core.mail.serializers import MailMessagePayloadSerializer


class MailService:
    """ Send outbound mail through the project's current delivery backend. """

    delivery_backend_class = DjangoMailDeliveryBackend
    payload_serializer_class = MailMessagePayloadSerializer

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

    @classmethod
    def send_async(cls, message: MailMessageDTO, fail_silently: bool = False) -> AsyncResult:
        """ Enqueue one outbound message for asynchronous delivery.

        Args:
            message: Outbound mail payload.
            fail_silently: Whether transport errors should be swallowed in the worker.

        Returns:
            AsyncResult: Celery async result handle for the queued task.
        """
        from core.tasks.mail.tasks import send_mail_message_task

        payload = cls.payload_serializer_class.serialize(message)
        return send_mail_message_task.delay(payload=payload, fail_silently=fail_silently)
