""" Tests for the composed admin active-tenant resolver. """

from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponse
from accounts.models import UserModel
from core.testing.base import LoggedTestCase
from tenancy.models import TenantMembershipModel, TenantModel
from tenancy.resolution import AdminActiveTenantResolver
from tenancy.resolution.strategies import PathTenantResolutionStrategy


class TestAdminActiveTenantResolver(LoggedTestCase):
    """ Verify the admin active-tenant resolver keeps current behavior unchanged. """

    def setUp(self) -> None:
        """ Create reusable user and memberships for strategy composition tests. """
        self.user = UserModel.objects.create_user(username="resolver-user", password="test-pass")
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

    def _build_request(self) -> HttpRequest:
        """ Build one session-backed request for active-tenant resolution tests.

        Returns:
            HttpRequest: Request with attached session.
        """
        request = HttpRequest()
        SessionMiddleware(lambda req: HttpResponse("ok")).process_request(request)
        request.session.save()
        request.user = self.user
        return request

    def test_resolver_prefers_session_before_membership_fallback(self) -> None:
        """ Verify the composed resolver keeps session-first behavior. """
        request = self._build_request()
        request.session["active_tenant_id"] = str(self.secondary_tenant.pk)

        tenant = AdminActiveTenantResolver.resolve(request)

        self.assertEqual(self.secondary_tenant, tenant)

    def test_resolver_falls_back_to_primary_membership_when_session_is_missing(self) -> None:
        """ Verify the composed resolver keeps membership fallback behavior. """
        request = self._build_request()

        tenant = AdminActiveTenantResolver.resolve(request)

        self.assertEqual(self.primary_tenant, tenant)
        self.assertEqual(str(self.primary_tenant.pk), request.session["active_tenant_id"])

    def test_path_strategy_remains_inactive_until_frontend_path_resolution_is_introduced(self) -> None:
        """ Verify the future path strategy stays dormant in the current runtime. """
        request = self._build_request()

        tenant = PathTenantResolutionStrategy.resolve(request)

        self.assertIsNone(tenant)
