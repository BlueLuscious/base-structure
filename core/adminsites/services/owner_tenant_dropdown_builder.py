""" Service for building the owner admin tenant switcher dropdown. """

from typing import TYPE_CHECKING, Any, cast
from django.apps import apps
from django.http import HttpRequest
from core.adminsites.services.active_tenant_switch_url_builder import ActiveTenantSwitchUrlBuilder

if TYPE_CHECKING:
    from tenancy.models import TenantMembershipModel


class OwnerTenantDropdownBuilder:
    """ Build tenant switcher dropdown items for the owner admin site. """

    switch_url_builder_class = ActiveTenantSwitchUrlBuilder

    @classmethod
    def get_membership_model(cls) -> type["TenantMembershipModel"]:
        """ Resolve the tenant-membership model without early ORM imports.

        Returns:
            type[TenantMembershipModel]: Runtime tenant-membership model class.
        """
        return cast(
            type["TenantMembershipModel"],
            apps.get_model("tenancy", "TenantMembershipModel"),
        )

    @classmethod
    def build(cls, request: HttpRequest) -> list[dict[str, Any]]:
        """ Build tenant switcher items for the owner admin site.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Dropdown items for active tenant memberships.
        """
        if not getattr(request.user, "is_authenticated", False):
            return []

        memberships = (
            cls.get_membership_model().objects.active()
            .filter(user=request.user, tenant__is_active=True)
            .select_related("tenant")
            .order_by("-is_primary", "tenant__name", "tenant__slug")
        )
        current_tenant_id = str(getattr(getattr(request, "tenant", None), "pk", ""))

        dropdown_items: list[dict[str, Any]] = []
        for membership in list(memberships):
            tenant = membership.tenant
            is_current_tenant = str(tenant.pk) == current_tenant_id
            title = f"{tenant.name} (Current)" if is_current_tenant else tenant.name

            dropdown_items.append(
                {
                    "title": title,
                    "link": cls.switch_url_builder_class.build(request, tenant),
                    "icon": "check_circle" if is_current_tenant else "domain",
                }
            )

        return dropdown_items
