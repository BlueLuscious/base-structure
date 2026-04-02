""" Tests for request-time active tenant resolution. """

from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponse
from core.testing.base import LoggedTestCase
from core.tenancy import ActiveTenantContext
from core.tenancy.middleware.active_tenant_middleware import ActiveTenantMiddleware
from accounts.models import UserModel
from tenancy.models import TenantMembershipModel, TenantModel


class TestActiveTenantMiddleware(LoggedTestCase):
    """ Verify middleware-based active tenant resolution. """

    def setUp(self) -> None:
        """ Create reusable users and tenants for middleware tests. """
        self.user = UserModel.objects.create_user(username="lucio", password="test-pass")
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
        self.middleware = ActiveTenantMiddleware(lambda request: HttpResponse("ok"))

    def _build_request(self) -> HttpRequest:
        """ Build a request with an attached session.

        Returns:
            HttpRequest: Request ready for middleware execution.
        """
        request = HttpRequest()
        SessionMiddleware(lambda req: HttpResponse("ok")).process_request(request)
        request.session.save()
        return request

    def test_middleware_falls_back_to_primary_tenant(self) -> None:
        """ Verify the middleware uses the primary tenant when the session has none. """
        request = self._build_request()
        request.user = self.user

        self.middleware(request)

        self.assertEqual(self.primary_tenant, request.tenant)
        self.assertEqual(str(self.primary_tenant.pk), request.session["active_tenant_id"])

    def test_middleware_keeps_session_tenant_when_membership_is_valid(self) -> None:
        """ Verify the middleware preserves a session-selected tenant when the user still belongs to it. """
        request = self._build_request()
        request.user = self.user
        request.session["active_tenant_id"] = str(self.secondary_tenant.pk)

        self.middleware(request)

        self.assertEqual(self.secondary_tenant, request.tenant)

    def test_middleware_clears_active_tenant_for_anonymous_users(self) -> None:
        """ Verify the middleware clears tenant state for anonymous requests. """
        request = self._build_request()
        request.user = type("AnonymousUserLike", (), {"is_authenticated": False})()
        request.session["active_tenant_id"] = str(self.primary_tenant.pk)

        self.middleware(request)

        self.assertIsNone(request.tenant)
        self.assertNotIn("active_tenant_id", request.session)

    def test_middleware_exposes_current_tenant_during_request_and_clears_it_afterwards(self) -> None:
        """ Verify the middleware sets the runtime tenant context only for the active request. """
        captured_tenant_names: list[str | None] = []
        middleware = ActiveTenantMiddleware(
            lambda request: captured_tenant_names.append(
                getattr(ActiveTenantContext.get(), "name", None)
            ) or HttpResponse("ok")
        )
        request = self._build_request()
        request.user = self.user

        middleware(request)

        self.assertEqual(["GEA Center"], captured_tenant_names)
        self.assertIsNone(ActiveTenantContext.get())
