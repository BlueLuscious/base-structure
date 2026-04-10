""" MailHog-backed integration tests for the templated mail service. """

from uuid import uuid4
from core.mail import MailRecipientDTO, TemplateMailService
from core.tests.mail.integration.base import BaseMailIntegrationSimpleTestCase


class TestMailhogTemplateMailServiceIntegration(BaseMailIntegrationSimpleTestCase):
    """ Verify the templated mail service can send real SMTP mail to MailHog. """

    def test_send_delivers_one_real_templated_message_to_mailhog(self) -> None:
        """ Deliver one real templated message and confirm MailHog captures it. """
        subject = f"MailHog templated single {uuid4()}"

        delivered_count = TemplateMailService.send(
            subject=subject,
            to=[MailRecipientDTO(email="integration@example.com", name="Integration User")],
            context={
                "mail_title": "Integration template",
                "mail_intro": "Hello from the templated integration flow.",
                "mail_body": "This message should appear in MailHog.",
                "mail_outro": "Regards from the template service.",
                "cta_label": "Open dashboard",
                "cta_url": "https://example.com/dashboard",
            },
            html_template_name="mail/messages/test_message.html",
            text_template_name="mail/messages/test_message.txt",
        )

        self.assertEqual(1, delivered_count)
        self.assertTrue(self.mailhog_contains_subject(subject))

    def test_send_delivers_multiple_real_templated_messages_to_mailhog(self) -> None:
        """ Deliver multiple templated messages and confirm MailHog captures both subjects. """
        first_subject = f"MailHog templated first {uuid4()}"
        second_subject = f"MailHog templated second {uuid4()}"

        first_delivered_count = TemplateMailService.send(
            subject=first_subject,
            to=[MailRecipientDTO(email="integration@example.com")],
            context={
                "mail_title": "First templated integration",
                "mail_body": "First templated body.",
            },
            html_template_name="mail/messages/test_message.html",
            text_template_name="mail/messages/test_message.txt",
        )
        second_delivered_count = TemplateMailService.send(
            subject=second_subject,
            to=[MailRecipientDTO(email="integration@example.com")],
            context={
                "mail_title": "Second templated integration",
                "mail_body": "Second templated body.",
            },
            html_template_name="mail/messages/test_message.html",
            text_template_name="mail/messages/test_message.txt",
        )

        self.assertEqual(1, first_delivered_count)
        self.assertEqual(1, second_delivered_count)
        self.assertEqual(1, self.mailhog_subject_count(first_subject))
        self.assertEqual(1, self.mailhog_subject_count(second_subject))
