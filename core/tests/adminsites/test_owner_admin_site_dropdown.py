""" Tests for the owner admin tenant switcher dropdown. """

from django.test import RequestFactory
from django.utils.translation import gettext as _
from core.adminsites.site_instances import owner_admin_site
from core.testing.base import LoggedTestCase
from accounts.models import UserModel
from tenancy.models import TenantMembershipModel, TenantModel


class TestOwnerAdminSiteDropdown(LoggedTestCase):
    """ Verify the owner admin site exposes a tenant switcher for active memberships. """

    def setUp(self) -> None:
        """ Create reusable users and tenants for owner admin dropdown coverage. """
        self.request_factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username="owner-user",
            password="test-pass",
            is_staff=True,
        )
        self.primary_tenant = TenantModel.objects.create(name="GEA Center", slug="gea-center")
        self.secondary_tenant = TenantModel.objects.create(name="North Center", slug="north-center")

        TenantMembershipModel.objects.create(
            tenant=self.primary_tenant,
            user=self.user,
            is_primary=True,
        )
        TenantMembershipModel.objects.create(
            tenant=self.secondary_tenant,
            user=self.user,
            is_primary=False,
        )

    def test_get_site_dropdown_returns_active_tenant_switch_links(self) -> None:
        """ Verify the owner admin site exposes one switch link per active tenant membership. """
        request = self.request_factory.get("/owner-admin/")
        request.user = self.user
        request.tenant = self.primary_tenant

        dropdown_items = owner_admin_site.get_site_dropdown(request)

        self.assertEqual(2, len(dropdown_items))
        self.assertEqual(f"GEA Center ({_('Current')})", dropdown_items[0]["title"])
        self.assertIn(str(self.primary_tenant.pk), dropdown_items[0]["link"])
        self.assertEqual("check_circle", dropdown_items[0]["icon"])
        self.assertEqual("North Center", dropdown_items[1]["title"])
        self.assertIn(str(self.secondary_tenant.pk), dropdown_items[1]["link"])
        self.assertEqual("domain", dropdown_items[1]["icon"])

    def test_get_site_dropdown_returns_empty_list_for_anonymous_like_users(self) -> None:
        """ Verify the owner admin dropdown stays empty when the user is not authenticated. """
        request = self.request_factory.get("/owner-admin/")
        request.user = type("AnonymousUserLike", (), {"is_authenticated": False})()
        request.tenant = None

        self.assertEqual([], owner_admin_site.get_site_dropdown(request))
