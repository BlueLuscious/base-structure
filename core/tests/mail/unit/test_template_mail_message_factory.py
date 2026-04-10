""" Tests for the templated mail message factory. """

from core.mail import MailRecipientDTO
from core.mail.factories import TemplateMailMessageFactory
from core.testing import LoggedSimpleTestCase


class TestTemplateMailMessageFactory(LoggedSimpleTestCase):
    """ Verify one template pair is converted into one outbound mail DTO. """

    def test_build_renders_text_html_and_keeps_routing_metadata(self) -> None:
        """ Build one outbound DTO preserving rendered bodies and reply metadata. """
        message = TemplateMailMessageFactory.build(
            subject="Template factory",
            to=[MailRecipientDTO(email="owner@example.com")],
            context={
                "mail_title": "Template factory",
                "mail_body": "Factory body",
                "cta_label": "Open dashboard",
                "cta_url": "https://example.com/dashboard",
            },
            html_template_name="mail/messages/test_message.html",
            text_template_name="mail/messages/test_message.txt",
            reply_to=["reply@example.com"],
            headers={"X-Test": "factory"},
        )

        self.assertEqual("Template factory", message.subject)
        self.assertIn("Factory body", message.text_body)
        self.assertIn("Factory body", str(message.html_body))
        self.assertNotIn("Sent via", message.text_body)
        self.assertNotIn("Sent via", str(message.html_body))
        self.assertEqual(("reply@example.com",), message.reply_to)
        self.assertEqual({"X-Test": "factory"}, message.headers)
