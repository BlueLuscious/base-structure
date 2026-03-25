""" Master admin site definition. """

from typing import Any
from django.http import HttpRequest
from django.urls import reverse_lazy
from core.adminsites.admin_namespace import AdminNamespace
from core.adminsites.sites.base_admin_site import BaseAdminSite


class MasterAdminSite(BaseAdminSite):
    """ Full admin site reserved for technical platform administrators. """

    settings_name = "MASTER_ADMIN_UNFOLD"
    site_header = "GEA Master Administration"
    site_title = "GEA Master Admin"
    site_symbol = "shield_person"
    index_title = "Platform administration"
    show_all_applications = True

    @classmethod
    def get_sidebar_navigation(cls, request: HttpRequest) -> list[dict[str, Any]]:
        """ Return master admin sidebar navigation.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Sidebar navigation groups for the master site.
        """
        namespace = AdminNamespace.MASTER

        return [
            {
                "title": "Accounts",
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy(f"{namespace}:accounts_usermodel_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": reverse_lazy(f"{namespace}:auth_group_changelist"),
                    },
                ],
            }
        ]

    def has_permission(self, request: HttpRequest) -> bool:
        """ Return whether the request user can access the master admin site.

        Args:
            request: Current admin request.

        Returns:
            bool: True when the request user is an active superuser.
        """
        user = request.user
        return bool(user.is_active and user.is_superuser)
