""" Tests for admin site Unfold configuration resolution. """

from django.test import RequestFactory
from core.adminsites.admin_namespace import AdminNamespace
from core.adminsites.sites.master_admin_site import MasterAdminSite
from core.adminsites.sites.owner_admin_site import OwnerAdminSite
from core.adminsites.unfold import AdminSiteUnfoldSettings
from core.testing.base import LoggedSimpleTestCase


class TestAdminSitesUnfold(LoggedSimpleTestCase):
    """ Cover request-based Unfold configuration for custom admin sites. """

    def setUp(self) -> None:
        """ Create the request factory used by the tests. """
        self.request_factory = RequestFactory()

    def test_resolve_admin_namespace_returns_none_without_resolver_match(self) -> None:
        """ Verify namespace resolution returns none when the request has no resolver match. """
        request = self.request_factory.get("/admin/")

        self.assertIsNone(AdminSiteUnfoldSettings.resolve_admin_namespace(request))

    def test_resolve_admin_site_class_dispatches_to_owner_namespace(self) -> None:
        """ Verify the request resolver namespace selects the owner admin site class. """
        request = self.request_factory.get("/owner-admin/")
        request.resolver_match = type("ResolverMatch", (), {"namespace": AdminNamespace.OWNER.value})()

        site_class = AdminSiteUnfoldSettings.resolve_admin_site_class(request)

        self.assertIs(site_class, OwnerAdminSite)

    def test_build_admin_site_unfold_settings_uses_site_metadata_for_static_values(self) -> None:
        """ Verify the generated settings dictionary reuses static metadata from the site class. """
        request = self.request_factory.get("/admin/")
        settings_dict = AdminSiteUnfoldSettings.for_namespace(AdminNamespace.MASTER).build()

        self.assertEqual(settings_dict["SITE_TITLE"](request), MasterAdminSite.get_site_title(request))
        self.assertEqual(settings_dict["SITE_HEADER"](request), MasterAdminSite.get_site_header(request))
        self.assertEqual(settings_dict["SITE_SYMBOL"](request), MasterAdminSite.get_site_symbol(request))
        self.assertEqual(settings_dict["SITE_URL"](request), MasterAdminSite.get_site_url(request))

    def test_build_admin_site_unfold_settings_keeps_dynamic_sidebar_and_assets(self) -> None:
        """ Verify the generated settings dictionary keeps request-aware hooks only where needed. """
        settings_dict = AdminSiteUnfoldSettings.for_namespace(AdminNamespace.MASTER).build()

        self.assertEqual(settings_dict["SIDEBAR"]["navigation"].__name__, "build_sidebar_navigation")
        self.assertEqual(settings_dict["SCRIPTS"].__name__, "scripts")
        self.assertEqual(settings_dict["STYLES"].__name__, "styles")
        self.assertTrue(settings_dict["SIDEBAR"]["show_all_applications"](self.request_factory.get("/admin/")))

    def test_master_admin_sidebar_navigation_includes_users_and_groups(self) -> None:
        """ Verify the master admin sidebar includes account management links. """
        request = self.request_factory.get("/admin/")
        navigation = MasterAdminSite.get_sidebar_navigation(request)

        self.assertEqual(len(navigation), 1)
        self.assertEqual(navigation[0]["title"], "Accounts")
        self.assertEqual(navigation[0]["items"][0]["title"], "Users")
        self.assertEqual(navigation[0]["items"][1]["title"], "Groups")
