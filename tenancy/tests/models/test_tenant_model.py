"""Model tests for tenant persistence."""

from uuid import UUID

from core.testing.base import LoggedTestCase
from tenancy.models import TenantModel


class TestTenantModel(LoggedTestCase):
    """Verify tenant persistence and representation."""

    def test_string_representation_uses_tenant_name(self) -> None:
        """Verify the tenant string representation stays human-friendly."""
        tenant = TenantModel.objects.create(name="Example Business", slug="example-business")

        self.assertEqual("Example Business", str(tenant))
        self.assertIsInstance(tenant.pk, UUID)

    def test_optional_contact_fields_persist_on_the_tenant(self) -> None:
        """Verify tenant operational contact metadata persists independently from visual branding."""
        tenant = TenantModel.objects.create(
            name="Example Business",
            slug="example-business",
            business_email="hello@example.test",
            support_email="support@example.test",
            phone_number="+54 11 5555 1234",
            website_url="https://example.test",
        )

        self.assertEqual("hello@example.test", tenant.business_email)
        self.assertEqual("support@example.test", tenant.support_email)
        self.assertEqual("+54 11 5555 1234", tenant.phone_number)
        self.assertEqual("https://example.test", tenant.website_url)
