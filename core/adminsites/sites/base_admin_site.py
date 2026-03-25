""" Shared base admin site for project-specific admin sites. """

from typing import Any
from django.http import HttpRequest
from unfold.sites import UnfoldAdminSite


class BaseAdminSite(UnfoldAdminSite):
    """ Shared project admin site with default Unfold metadata and hooks. """

    site_symbol = ""
    site_url = "/"
    show_all_applications = False
    show_sidebar_search = True
    dashboard_callback: str | None = None

    @classmethod
    def get_site_title(cls, request: HttpRequest) -> str:
        """ Return the site title for the current request.

        Args:
            request: Current admin request.

        Returns:
            str: Site title.
        """
        return cls.site_title

    @classmethod
    def get_site_header(cls, request: HttpRequest) -> str:
        """ Return the site header for the current request.

        Args:
            request: Current admin request.

        Returns:
            str: Site header.
        """
        return cls.site_header

    @classmethod
    def get_site_symbol(cls, request: HttpRequest) -> str:
        """ Return the site symbol for the current request.

        Args:
            request: Current admin request.

        Returns:
            str: Site symbol.
        """
        return cls.site_symbol

    @classmethod
    def get_site_url(cls, request: HttpRequest) -> str:
        """ Return the site URL for the current request.

        Args:
            request: Current admin request.

        Returns:
            str: Site URL.
        """
        return cls.site_url

    @classmethod
    def get_show_all_applications(cls, request: HttpRequest) -> bool:
        """ Return whether the site should show all applications.

        Args:
            request: Current admin request.

        Returns:
            bool: True when all applications should be shown.
        """
        return cls.show_all_applications

    @classmethod
    def get_show_sidebar_search(cls, request: HttpRequest) -> bool:
        """ Return whether the site should show sidebar search.

        Args:
            request: Current admin request.

        Returns:
            bool: True when sidebar search should be shown.
        """
        return cls.show_sidebar_search

    @classmethod
    def get_dashboard_callback(cls, request: HttpRequest) -> str | None:
        """ Return the dashboard callback for the current request.

        Args:
            request: Current admin request.

        Returns:
            str | None: Dashboard callback path when configured.
        """
        return cls.dashboard_callback

    @classmethod
    def get_sidebar_navigation(cls, request: HttpRequest) -> list[dict[str, Any]]:
        """ Return sidebar navigation items for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[dict[str, Any]]: Sidebar navigation items.
        """
        return []

    @classmethod
    def get_scripts(cls, request: HttpRequest) -> list[str]:
        """ Return additional Unfold script paths for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[str]: Script asset paths.
        """
        return []

    @classmethod
    def get_styles(cls, request: HttpRequest) -> list[str]:
        """ Return additional Unfold style paths for the current request.

        Args:
            request: Current admin request.

        Returns:
            list[str]: Style asset paths.
        """
        return []
