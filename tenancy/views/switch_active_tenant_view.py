""" Class-based view for explicit active-tenant switching. """

from uuid import UUID
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from tenancy.services import ActiveTenantSwitcher


class SwitchActiveTenantView(LoginRequiredMixin, View):
    """ Switch the active tenant for the current authenticated user through one GET request. """

    http_method_names = ["get"]

    def get(self, request: HttpRequest, tenant_id: UUID) -> HttpResponse:
        """ Switch the active tenant for the current authenticated user.

        Args:
            request: Current HTTP request.
            tenant_id: Tenant identifier requested by the user.

        Returns:
            HttpResponse: Redirect response to the requested ``next`` location or the owner admin.
        """
        ActiveTenantSwitcher.switch(request, tenant_id)

        next_url = request.GET.get("next", "")
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)

        return redirect(reverse("owner_admin:index"))
