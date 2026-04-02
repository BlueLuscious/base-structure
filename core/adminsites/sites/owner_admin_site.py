""" Owner admin site definition. """

from typing import Any
from django.http import HttpRequest
from django.urls import reverse
from core.adminsites.services import OwnerTenantDropdownBuilder
from core.adminsites.sites.base_admin_site import BaseAdminSite
from tenancy.services.tenant_accounts_access_policy import TenantAccountsAccessPolicy


class OwnerAdminSite(BaseAdminSite):
    """ Guided admin site intended for business owners and operators. """

    settings_name = "OWNER_ADMIN_UNFOLD"
    site_header = "Owner Administration"
    site_title = "Owner Admin"
    site_symbol = "storefront"
    index_title = "Business operations"

    @classmethod
    def get_site_title(cls, request: HttpRequest) -> str:
        """ Return the owner site title, preferring the active tenant name.

        Args:
            request: Current admin request.

        Returns:
            str: Tenant-aware site title.
        """
        tenant = getattr(request, "tenant", None)
        tenant_name = getattr(tenant, "name", "")
        if tenant_name:
            return str(tenant_name)
        return super().get_site_title(request)

    @classmethod
    def get_site_header(cls, request: HttpRequest) -> str:
        """ Return the owner site header, preferring the active tenant name.

        Args:
            request: Current admin request.

        Returns:
            str: Tenant-aware site header.
        """
        tenant = getattr(request, "tenant", None)
        tenant_name = getattr(tenant, "name", "")
        if tenant_name:
            return f"{tenant_name} Administration"
        return super().get_site_header(request)

    def has_permission(self, request: HttpRequest) -> bool:
        """ Return whether the request user can access the owner admin site.

        Args:
            request: Current admin request.

        Returns:
            bool: True when the request user is an active staff user.
        """
        user = request.user
        return bool(user.is_active and user.is_staff)

    def get_site_dropdown(self, request: HttpRequest) -> list[dict[str, Any]]:
        """ Return tenant switcher items for the current owner admin request.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Dropdown items for active tenant memberships.
        """
        return OwnerTenantDropdownBuilder.build(request)

    def get_sidebar_navigation(self, request: HttpRequest) -> list[dict[str, Any]]:
        """ Return owner sidebar navigation for account administration.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Sidebar navigation groups for the owner site.
        """
        return [
            {
                "title": "Accounts",
                "items": [
                    {
                        "title": "Users",
                        "icon": "group",
                        "link": reverse("owner_admin:accounts_usermodel_changelist"),
                        "permission": lambda req: (
                            TenantAccountsAccessPolicy.can_manage_accounts(req)
                            and req.user.has_perm("accounts.view_usermodel")
                        ),
                    },
                    {
                        "title": "Groups",
                        "icon": "admin_panel_settings",
                        "link": reverse("owner_admin:auth_group_changelist"),
                        "permission": lambda req: (
                            TenantAccountsAccessPolicy.can_manage_accounts(req)
                            and req.user.has_perm("auth.view_group")
                        ),
                    },
                ]
            },
        ]
