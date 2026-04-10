""" Tests for the templated mail service. """

from django.core import mail
from django.test import override_settings
from core.mail import MailRecipientDTO, TemplateMailService
from core.testing import LoggedSimpleTestCase


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class TestTemplateMailService(LoggedSimpleTestCase):
    """ Verify templated mail is rendered and delivered through the mail service. """

    def setUp(self) -> None:
        """ Reset the in-memory outbox before each test.

        Returns:
            None
        """
        super().setUp()
        mail.outbox = []

    def test_send_delivers_one_rendered_template_message(self) -> None:
        """ Deliver one templated message through the configured backend. """
        delivered_count = TemplateMailService.send(
            subject="Template mail service",
            to=[MailRecipientDTO(email="owner@example.com", name="Owner User")],
            context={
                "mail_title": "Template mail service",
                "mail_intro": "Hello there.",
                "mail_body": "This message comes from one Django template.",
                "mail_outro": "See you soon.",
                "cta_label": "Open dashboard",
                "cta_url": "https://example.com/dashboard",
            },
            html_template_name="mail/messages/test_message.html",
            text_template_name="mail/messages/test_message.txt",
        )

        self.assertEqual(1, delivered_count)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual("Template mail service", mail.outbox[0].subject)
        self.assertIn("This message comes from one Django template.", mail.outbox[0].body)
        self.assertNotIn("Sent via", mail.outbox[0].body)
        self.assertEqual(1, len(mail.outbox[0].alternatives))
        self.assertIn("Open dashboard", mail.outbox[0].alternatives[0][0])
