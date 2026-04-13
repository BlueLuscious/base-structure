""" Project-wide Celery tasks for outbound mail delivery. """

from celery import shared_task
from core.mail.serializers import MailMessagePayloadSerializer, TemplateMailRequestPayloadSerializer
from core.mail.services import MailService, TemplateMailService


@shared_task(name="core.tasks.mail.send_mail_message_task")
def send_mail_message_task(payload: dict, fail_silently: bool = False) -> int:
    """ Rebuild one raw mail payload and send it through the project mail service.

    Args:
        payload: Serialized outbound mail payload.
        fail_silently: Whether transport errors should be swallowed.

    Returns:
        int: Number of successfully delivered messages.
    """
    message = MailMessagePayloadSerializer.deserialize(payload)
    return MailService.send(message, fail_silently=fail_silently)


@shared_task(name="core.tasks.mail.send_templated_mail_task")
def send_templated_mail_task(payload: dict, fail_silently: bool = False) -> int:
    """ Rebuild one templated mail payload and send it through the templated mail service.

    Args:
        payload: Serialized templated mail payload.
        fail_silently: Whether transport errors should be swallowed.

    Returns:
        int: Number of successfully delivered messages.
    """
    request = TemplateMailRequestPayloadSerializer.deserialize(payload)
    return TemplateMailService.send(request, fail_silently=fail_silently)
