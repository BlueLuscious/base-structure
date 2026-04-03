""" Tests for the tenant accounts access policy. """

from django.contrib.auth.models import Group
from django.test import RequestFactory
from core.testing.base import LoggedTestCase
from accounts.models import UserModel
from tenancy.choices import TenantRole
from tenancy.models import TenantGroupModel, TenantMembershipModel, TenantModel
from tenancy.access.tenant_accounts_access_policy import TenantAccountsAccessPolicy


class TestTenantAccountsAccessPolicy(LoggedTestCase):
    """ Verify tenant accounts access checks stay aligned with tenant scope. """

    def setUp(self) -> None:
        """ Build one owner request with active tenant scope. """
        self.request_factory = RequestFactory()
        self.owner = UserModel.objects.create_user(
            username="owner",
            password="test-pass",
            is_active=True,
            is_staff=True,
        )
        self.operator = UserModel.objects.create_user(
            username="operator",
            password="test-pass",
            is_active=True,
            is_staff=True,
        )
        self.platform_member = UserModel.objects.create_user(
            username="platform-member",
            password="test-pass",
            is_active=True,
            is_staff=True,
        )
        self.tenant = TenantModel.objects.create(name="GEA Center", slug="gea-center")
        self.other_tenant = TenantModel.objects.create(name="Other Center", slug="other-center")
        TenantMembershipModel.objects.create(
            tenant=self.tenant,
            user=self.owner,
            role=TenantRole.OWNER,
            is_active=True,
            is_primary=True,
        )
        TenantMembershipModel.objects.create(
            tenant=self.tenant,
            user=self.operator,
            role=TenantRole.OPERATOR,
            is_active=True,
        )
        TenantMembershipModel.objects.create(
            tenant=self.tenant,
            user=self.platform_member,
            role=TenantRole.MASTER,
            is_active=True,
        )
        self.group = Group.objects.create(name="Sales")
        TenantGroupModel.objects.create(tenant=self.tenant, group=self.group)

    def build_request(self) -> object:
        """ Build one request scoped to the active tenant. """
        request = self.request_factory.get("/owner-admin/")
        request.user = self.owner
        request.tenant = self.tenant
        return request

    def test_can_manage_accounts_returns_true_for_owner(self) -> None:
        """ Verify active tenant owners may manage accounts. """
        self.assertTrue(TenantAccountsAccessPolicy.can_manage_accounts(self.build_request()))

    def test_can_view_user_returns_false_for_master_membership(self) -> None:
        """ Verify platform members remain hidden from owner accounts admin. """
        self.assertFalse(TenantAccountsAccessPolicy.can_view_user(self.build_request(), self.platform_member))

    def test_can_view_group_returns_true_for_group_bound_to_active_tenant(self) -> None:
        """ Verify tenant-bound groups remain visible in owner accounts admin. """
        self.assertTrue(TenantAccountsAccessPolicy.can_view_group(self.build_request(), self.group))
