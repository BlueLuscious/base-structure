""" Service for building active-tenant switch URLs. """

from typing import TYPE_CHECKING
from django.http import HttpRequest
from django.urls import NoReverseMatch, ResolverMatch, reverse
from django.utils.http import urlencode

if TYPE_CHECKING:
    from tenancy.models import TenantModel


class ActiveTenantSwitchUrlBuilder:
    """ Build safe active-tenant switch URLs for the current request context. """

    @classmethod
    def build(cls, request: HttpRequest, tenant: "TenantModel") -> str:
        """ Build one tenant switch URL including one safe return target.

        Args:
            request: Current admin request.
            tenant: Tenant that should become active after the switch.

        Returns:
            str: Absolute application URL for the active-tenant switch flow.
        """
        next_path = cls._build_next_path(request, tenant)
        return (
            f"{reverse('switch-active-tenant', kwargs={'tenant_id': tenant.pk})}"
            f"?{urlencode({'next': next_path})}"
        )

    @classmethod
    def _build_next_path(cls, request: HttpRequest, tenant: "TenantModel") -> str:
        """ Build one portable ``next`` path for the target tenant.

        Args:
            request: Current admin request.
            tenant: Tenant that should become active after the switch.

        Returns:
            str: Portable return path for the switch redirect.
        """
        resolver_match: ResolverMatch | None = getattr(request, "resolver_match", None)
        if resolver_match is None:
            return request.get_full_path()

        tenant_change_path = cls._build_tenant_change_path(request, resolver_match, tenant)
        if tenant_change_path is not None:
            return tenant_change_path

        change_fallback_path = cls._build_change_view_fallback_path(resolver_match)
        if change_fallback_path is not None:
            return change_fallback_path

        return request.get_full_path()

    @classmethod
    def _build_tenant_change_path(cls, request: HttpRequest, resolver_match: ResolverMatch, tenant: "TenantModel") -> str | None:
        """ Rebuild the active-tenant business settings screen for the target tenant.

        Args:
            request: Current admin request.
            resolver_match: Resolved route metadata for the current request.
            tenant: Tenant that should become active after the switch.

        Returns:
            str | None: Target tenant change path when the current screen is the
            active-tenant business settings screen, otherwise ``None``.
        """
        current_tenant: "TenantModel | None" = getattr(request, "tenant", None)
        current_tenant_id = str(getattr(current_tenant, "pk", ""))
        object_id = str(resolver_match.kwargs.get("object_id", ""))

        if resolver_match.view_name != "owner_admin:tenancy_tenantmodel_change":
            return None

        if not current_tenant_id or object_id != current_tenant_id:
            return None

        return reverse(
            "owner_admin:tenancy_tenantmodel_change",
            kwargs={"object_id": str(tenant.pk)},
        )

    @classmethod
    def _build_change_view_fallback_path(cls, resolver_match: ResolverMatch) -> str | None:
        """ Build one portable fallback for non-tenant admin change views.

        Args:
            resolver_match: Resolved route metadata for the current request.

        Returns:
            str | None: Changelist or index path when the current route is one
            change view, otherwise ``None``.
        """
        if not resolver_match.url_name.endswith("_change"):
            return None

        changelist_url_name = resolver_match.url_name.removesuffix("_change") + "_changelist"
        view_name = changelist_url_name
        if resolver_match.namespace:
            view_name = f"{resolver_match.namespace}:{changelist_url_name}"

        try:
            return reverse(view_name)
        except NoReverseMatch:
            if resolver_match.namespace:
                return reverse(f"{resolver_match.namespace}:index")

        return reverse("owner_admin:index")
