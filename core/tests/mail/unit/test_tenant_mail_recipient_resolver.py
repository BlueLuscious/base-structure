"""Tests for tenant-aware mail recipient resolution."""

from core.mail import TenantMailRecipientResolver
from core.testing import LoggedSimpleTestCase
from tenancy.models import TenantBrandingModel, TenantModel


class TestTenantMailRecipientResolver(LoggedSimpleTestCase):
    """Verify tenant-facing contact recipients resolve from tenant metadata."""

    def test_resolve_contact_email_prefers_support_email(self) -> None:
        """Resolve the preferred contact email from support email before business email."""
        tenant = TenantModel(
            name="Example Company",
            slug="example-company",
            business_email="hello@example.test",
            support_email="support@example.test",
        )

        self.assertEqual(
            "support@example.test",
            TenantMailRecipientResolver.resolve_contact_email(tenant),
        )

    def test_resolve_contact_recipient_uses_display_name_when_branding_exists(self) -> None:
        """Build one tenant-facing recipient with the preferred business display name."""
        tenant = TenantModel(
            name="Example Company Legal",
            slug="example-company-legal",
            business_email="hello@example.test",
        )
        branding = TenantBrandingModel(
            tenant=tenant,
            display_name="Example Company",
        )
        tenant._state.fields_cache["branding"] = branding

        recipient = TenantMailRecipientResolver.resolve_contact_recipient(tenant)

        self.assertIsNotNone(recipient)
        self.assertEqual("hello@example.test", recipient.email)
        self.assertEqual("Example Company", recipient.name)
