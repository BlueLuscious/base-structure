""" Tests for the mail template renderer. """

from core.mail.template_renderer import MailTemplateRenderer
from core.testing import LoggedSimpleTestCase


class TestMailTemplateRenderer(LoggedSimpleTestCase):
    """ Verify mail templates render with the expected base context. """

    def test_render_text_keeps_the_output_neutral_when_no_branding_context_exists(self) -> None:
        """ Render the text template without inventing product or support branding. """
        rendered_text = MailTemplateRenderer.render_text(
            "mail/messages/test_message.txt",
            {
                "mail_title": "Renderer test",
                "mail_body": "Plain text body",
            },
        )

        self.assertIn("Renderer test", rendered_text)
        self.assertIn("Plain text body", rendered_text)
        self.assertNotIn("Sent via", rendered_text)
        self.assertNotIn("Support:", rendered_text)

    def test_render_html_keeps_the_output_neutral_when_no_branding_context_exists(self) -> None:
        """ Render the HTML template without inventing product or support branding. """
        rendered_html = MailTemplateRenderer.render_html(
            "mail/messages/test_message.html",
            {
                "mail_title": "Renderer test",
                "mail_body": "HTML body",
            },
        )

        self.assertIn("Renderer test", rendered_html)
        self.assertIn("HTML body", rendered_html)
        self.assertNotIn("Sent via", rendered_html)
        self.assertNotIn("Support:", rendered_html)

    def test_render_html_includes_branding_when_context_provides_it(self) -> None:
        """ Render the HTML template with explicit product and support branding context. """
        rendered_html = MailTemplateRenderer.render_html(
            "mail/messages/test_message.html",
            {
                "mail_title": "Renderer test",
                "mail_body": "HTML body",
                "product_name": "Northwind Traders",
                "support_email": "support@northwind.test",
            },
        )

        self.assertIn("Northwind Traders", rendered_html)
        self.assertIn("support@northwind.test", rendered_html)
