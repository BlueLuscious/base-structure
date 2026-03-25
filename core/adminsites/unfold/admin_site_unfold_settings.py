""" Site-based Unfold settings adapter. """

from typing import Any
from django.http import HttpRequest
from django.utils.module_loading import import_string
from core.adminsites.admin_namespace import AdminNamespace
from core.adminsites.registry import ADMIN_SITE_REGISTRY
from core.adminsites.sites.base_admin_site import BaseAdminSite


class AdminSiteUnfoldSettings:
    """ Build an Unfold settings dictionary from an admin site class. """

    def __init__(self, site_class: type[BaseAdminSite], namespace: AdminNamespace) -> None:
        """ Store the admin site class used as the settings source of truth.

        Args:
            site_class: Admin site class that provides metadata and hooks.
            namespace: Namespace mapped to the admin site class.
        """
        self.site_class = site_class
        self.namespace = namespace

    @classmethod
    def for_namespace(cls, namespace: AdminNamespace) -> "AdminSiteUnfoldSettings":
        """ Build the adapter for one admin namespace.

        Args:
            namespace: Target admin namespace.

        Returns:
            AdminSiteUnfoldSettings: Adapter bound to the resolved admin site class.
        """
        site_class = cls._resolve_admin_site_class_for_namespace(namespace)
        return cls(site_class, namespace)

    def build(self) -> dict[str, Any]:
        """ Build the Unfold settings dictionary for the admin site class.

        Returns:
            dict[str, Any]: Unfold settings dictionary.
        """
        return {
            "SITE_TITLE": self.site_class.get_site_title,
            "SITE_HEADER": self.site_class.get_site_header,
            "SITE_SYMBOL": self.site_class.get_site_symbol,
            "SITE_URL": self.site_class.get_site_url,
            "SIDEBAR": {
                "show_search": self.site_class.get_show_sidebar_search,
                "show_all_applications": self.site_class.get_show_all_applications,
                "navigation": self.build_sidebar_navigation,
            },
            "SCRIPTS": self.scripts,
            "STYLES": self.styles,
            "DASHBOARD_CALLBACK": self.site_class.dashboard_callback,
        }

    @classmethod
    def resolve_admin_namespace(cls, request: HttpRequest) -> AdminNamespace | None:
        """ Resolve the current admin namespace from the request.

        Args:
            request: Current HTTP request.

        Returns:
            AdminNamespace | None: Resolved namespace when available.
        """
        resolver_match = request.resolver_match

        if resolver_match is None or not resolver_match.namespace:
            return None

        try:
            return AdminNamespace(resolver_match.namespace)
        except ValueError:
            return None

    @classmethod
    def resolve_admin_site_class(cls, request: HttpRequest) -> type[BaseAdminSite]:
        """ Resolve the current admin site class from the request.

        Args:
            request: Current HTTP request.

        Returns:
            type[BaseAdminSite]: Resolved admin site class.
        """
        namespace = cls.resolve_admin_namespace(request) or AdminNamespace.MASTER
        return cls._resolve_admin_site_class_for_namespace(namespace)

    @classmethod
    def build_sidebar_navigation(cls, request: HttpRequest) -> list[dict[str, Any]]:
        """ Return sidebar navigation for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Sidebar navigation items.
        """
        site_class = cls.resolve_admin_site_class(request)
        return site_class.get_sidebar_navigation(request)

    @classmethod
    def scripts(cls, request: HttpRequest) -> list[str]:
        """ Return additional Unfold script paths for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[str]: Script asset paths.
        """
        site_class = cls.resolve_admin_site_class(request)
        return site_class.get_scripts(request)

    @classmethod
    def styles(cls, request: HttpRequest) -> list[str]:
        """ Return additional Unfold style paths for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[str]: Style asset paths.
        """
        site_class = cls.resolve_admin_site_class(request)
        return site_class.get_styles(request)

    @classmethod
    def _resolve_admin_site_class_for_namespace(cls, namespace: AdminNamespace) -> type[BaseAdminSite]:
        """ Resolve an admin site class from an explicit namespace.

        Args:
            namespace: Target admin namespace.

        Returns:
            type[BaseAdminSite]: Resolved admin site class.
        """
        return import_string(ADMIN_SITE_REGISTRY[namespace])
