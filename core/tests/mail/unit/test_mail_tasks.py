""" Tests for project-wide asynchronous mail tasks. """

from unittest.mock import patch
from uuid import uuid4
from core.tasks.mail.tasks import send_mail_message_task, send_templated_mail_task
from core.testing import LoggedTestCase
from tenancy.models import TenantModel


class TestMailTasks(LoggedTestCase):
    """ Verify project-wide mail tasks rebuild payloads and delegate to mail services. """

    def test_send_mail_message_task_rebuilds_the_payload_and_delegates_to_the_mail_service(self) -> None:
        """ Rebuild one raw mail payload inside the task before delegating to the mail service. """
        with patch("core.tasks.mail.tasks.MailService.send", return_value=1) as send_mock:
            delivered_count = send_mail_message_task(
                payload={
                    "subject": "Task test",
                    "to": [{"email": "owner@example.com", "name": "Owner User"}],
                    "text_body": "Plain body",
                    "html_body": "<p>Plain body</p>",
                    "from_email": None,
                    "cc": [],
                    "bcc": [],
                    "reply_to": [],
                    "headers": {},
                    "attachments": [],
                },
                fail_silently=True,
            )

        self.assertEqual(1, delivered_count)
        self.assertEqual("Task test", send_mock.call_args.args[0].subject)
        self.assertTrue(send_mock.call_args.kwargs["fail_silently"])

    def test_send_templated_mail_task_rebuilds_the_payload_and_delegates_to_the_templated_service(self) -> None:
        """ Rebuild one templated mail payload inside the task before delegating to the templated mail service. """
        tenant = TenantModel.objects.create(
            name="GEA Trader",
            slug=f"gea-trader-{uuid4()}",
            business_email="hello@gea-trader.test",
        )

        with patch("core.tasks.mail.tasks.TemplateMailService.send", return_value=1) as send_mock:
            delivered_count = send_templated_mail_task(
                payload={
                    "subject": "Task test",
                    "to": [{"email": "owner@example.com", "name": "Owner User"}],
                    "context": {
                        "product_name": "GEA Trader",
                        "support_email": "hello@gea-trader.test",
                        "mail_title": "Task test",
                        "mail_body": "Template body",
                    },
                    "html_template_name": "mail/messages/test_message.html",
                    "text_template_name": "mail/messages/test_message.txt",
                    "from_email": None,
                    "cc": [],
                    "bcc": [],
                    "reply_to": [],
                    "headers": {},
                    "attachments": [],
                },
                fail_silently=True,
            )

        self.assertEqual(1, delivered_count)
        self.assertEqual("Task test", send_mock.call_args.args[0].subject)
        self.assertIsNone(send_mock.call_args.args[0].tenant)
        self.assertEqual("GEA Trader", send_mock.call_args.args[0].context["product_name"])
        self.assertTrue(send_mock.call_args.kwargs["fail_silently"])
