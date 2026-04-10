""" Shared helpers for MailHog-backed mail integration tests. """

import json
import os
from unittest import SkipTest
from urllib.request import urlopen
from django.conf import settings
from django.test import override_settings
from core.mail import MailMessageDTO, MailRecipientDTO, MailService
from core.testing import LoggedSimpleTestCase


def is_mail_integration_enabled() -> bool:
    """ Return whether mail integration tests should run.

    Returns:
        bool: True when mail integration tests are explicitly enabled.
    """
    return os.environ.get("RUN_MAIL_INTEGRATION_TESTS", "False").lower() in ("1", "true", "yes", "on")


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend",
    EMAIL_HOST="127.0.0.1",
    EMAIL_PORT=1025,
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class BaseMailIntegrationSimpleTestCase(LoggedSimpleTestCase):
    """ Define shared MailHog-backed integration helpers for outbound mail. """

    mailhog_messages_url = os.environ.get("MAILHOG_MESSAGES_API_URL", "http://127.0.0.1:8025/api/v2/messages")

    @classmethod
    def setUpClass(cls) -> None:
        """ Skip the suite when MailHog integration is not explicitly enabled. """
        super().setUpClass()

        if not is_mail_integration_enabled():
            raise SkipTest("Mail integration tests are disabled.")

        if settings.EMAIL_BACKEND != "django.core.mail.backends.smtp.EmailBackend":
            raise SkipTest("Mail integration tests require the SMTP email backend.")

    @classmethod
    def fetch_mailhog_messages(cls) -> list[dict[str, object]]:
        """ Fetch the current MailHog message list through its HTTP API.

        Returns:
            list[dict[str, object]]: MailHog message payloads.
        """
        with urlopen(cls.mailhog_messages_url) as response:
            payload = json.loads(response.read().decode())

        return list(payload.get("items", []))

    @classmethod
    def build_unique_message(cls, subject: str, body: str) -> MailMessageDTO:
        """ Build one integration mail payload with a unique recipient target.

        Args:
            subject: Unique subject for the integration mail.
            body: Plain-text body.

        Returns:
            MailMessageDTO: Outbound test payload.
        """
        return MailMessageDTO(
            subject=subject,
            to=[MailRecipientDTO(email="integration@example.com", name="Integration User")],
            text_body=body,
        )

    @classmethod
    def mailhog_contains_subject(cls, subject: str) -> bool:
        """ Return whether MailHog currently stores one message with the target subject.

        Args:
            subject: Subject to find in MailHog.

        Returns:
            bool: True when one captured message matches the subject.
        """
        for item in cls.fetch_mailhog_messages():
            content = item.get("Content", {})
            headers = content.get("Headers", {}) if isinstance(content, dict) else {}
            subjects = headers.get("Subject", []) if isinstance(headers, dict) else []

            if subject in subjects:
                return True

        return False

    @classmethod
    def mailhog_subject_count(cls, subject: str) -> int:
        """ Count how many captured MailHog messages match one subject.

        Args:
            subject: Subject to count.

        Returns:
            int: Number of MailHog messages carrying the subject.
        """
        matches = 0

        for item in cls.fetch_mailhog_messages():
            content = item.get("Content", {})
            headers = content.get("Headers", {}) if isinstance(content, dict) else {}
            subjects = headers.get("Subject", []) if isinstance(headers, dict) else []

            if subject in subjects:
                matches += 1

        return matches
