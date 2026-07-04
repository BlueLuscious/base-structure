"""HTTP smoke tests for the project admin sites."""

from django.test import override_settings

from accounts.models import UserModel
from core.testing.base import LoggedTestCase
from tenancy.choices import TenantRole
from tenancy.models import TenantMembershipModel, TenantModel


@override_settings(ALLOWED_HOSTS=["testserver"])
class TestAdminSiteSmoke(LoggedTestCase):
    """Verify both configured admin sites render for their intended users."""

    def setUp(self) -> None:
        """Create neutral users and tenant access for both admin surfaces."""
        self.superuser = UserModel.objects.create_superuser(
            username="technical-admin",
            email="technical-admin@example.test",
            password="test-password",
        )
        self.owner = UserModel.objects.create_user(
            username="tenant-owner",
            email="tenant-owner@example.test",
            password="test-password",
            is_staff=True,
        )
        self.tenant = TenantModel.objects.create(
            name="Example Business",
            slug="example-business",
        )
        TenantMembershipModel.objects.create(
            tenant=self.tenant,
            user=self.owner,
            role=TenantRole.OWNER,
            is_active=True,
            is_primary=True,
        )

    def test_master_admin_index_renders_for_superuser(self) -> None:
        """Verify an active superuser can render the technical admin index."""
        self.client.force_login(self.superuser)

        response = self.client.get("/admin/")

        self.assertEqual(200, response.status_code)
        self.assertEqual("master_admin", response.resolver_match.namespace)

    def test_owner_admin_index_renders_for_primary_tenant_owner(self) -> None:
        """Verify a staff owner with a primary membership can render owner admin."""
        self.client.force_login(self.owner)

        response = self.client.get("/owner-admin/")

        self.assertEqual(200, response.status_code)
        self.assertEqual("owner_admin", response.resolver_match.namespace)
        self.assertEqual(self.tenant, response.wsgi_request.tenant)
