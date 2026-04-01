""" QuerySet tests for tenant membership filters. """

from core.testing.base import LoggedTestCase
from accounts.models import UserModel
from tenancy.choices import TenantRole
from tenancy.models import TenantMembershipModel, TenantModel


class TestTenantMembershipModelQuerySet(LoggedTestCase):
    """ Verify reusable tenant membership queryset helpers. """

    def setUp(self) -> None:
        """ Create reusable memberships for queryset tests. """
        self.user = UserModel.objects.create_user(username="lucio", password="test-pass")
        self.other_user = UserModel.objects.create_user(username="sofia", password="test-pass")
        self.tenant = TenantModel.objects.create(name="GEA Center", slug="gea-center")
        self.other_tenant = TenantModel.objects.create(name="Other Center", slug="other-center")
        self.owner_membership = TenantMembershipModel.objects.create(
            tenant=self.tenant,
            user=self.user,
            role=TenantRole.OWNER,
            is_active=True,
            is_primary=True,
        )
        self.inactive_membership = TenantMembershipModel.objects.create(
            tenant=self.other_tenant,
            user=self.other_user,
            role=TenantRole.MASTER,
            is_active=False,
        )

    def test_active_filters_only_active_memberships(self) -> None:
        """ Verify active memberships exclude inactive rows. """
        self.assertEqual([self.owner_membership], list(TenantMembershipModel.objects.active()))

    def test_for_user_filters_memberships_by_user(self) -> None:
        """ Verify memberships can be filtered by user. """
        self.assertEqual([self.owner_membership], list(TenantMembershipModel.objects.for_user(self.user)))

    def test_for_tenant_filters_memberships_by_tenant(self) -> None:
        """ Verify memberships can be filtered by tenant. """
        self.assertEqual([self.owner_membership], list(TenantMembershipModel.objects.for_tenant(self.tenant)))

    def test_primary_filters_only_primary_memberships(self) -> None:
        """ Verify primary memberships filter excludes non-primary rows. """
        self.assertEqual([self.owner_membership], list(TenantMembershipModel.objects.primary()))

    def test_owners_filters_only_owner_memberships(self) -> None:
        """ Verify owner memberships filter excludes non-owner rows. """
        self.assertEqual([self.owner_membership], list(TenantMembershipModel.objects.owners()))
