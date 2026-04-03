""" Tests for admin site Unfold configuration resolution. """

from django.test import RequestFactory
from tenancy.models import TenantModel
from core.adminsites.admin_namespace import AdminNamespace
from core.adminsites.site_instances import owner_admin_site
from core.adminsites.site_instances import master_admin_site
from core.adminsites.sites.master_admin_site import MasterAdminSite
from core.adminsites.unfold import AdminSiteUnfoldCallbacks
from core.adminsites.unfold import AdminSiteUnfoldSettings
from core.testing.base import LoggedSimpleTestCase


class TestAdminSitesUnfold(LoggedSimpleTestCase):
    """ Cover request-based Unfold configuration for custom admin sites. """

    def setUp(self) -> None:
        """ Create the request factory used by the tests. """
        self.request_factory = RequestFactory()

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

        self.assertEqual(settings_dict["SITE_TITLE"].__name__, "site_title")
        self.assertEqual(settings_dict["SITE_HEADER"].__name__, "site_header")
        self.assertEqual(settings_dict["SITE_SYMBOL"].__name__, "site_symbol")
        self.assertEqual(settings_dict["SITE_URL"].__name__, "site_url")
        self.assertEqual(settings_dict["SITE_DROPDOWN"].__name__, "site_dropdown")
        self.assertEqual(settings_dict["SIDEBAR"]["navigation"].__name__, "sidebar_navigation")
        self.assertEqual(settings_dict["SCRIPTS"].__name__, "scripts")
        self.assertEqual(settings_dict["STYLES"].__name__, "styles")
        self.assertTrue(settings_dict["SIDEBAR"]["show_all_applications"](self.request_factory.get("/admin/")))

    def test_dynamic_callbacks_dispatch_to_owner_site_instance(self) -> None:
        """ Verify dynamic callbacks resolve the owner admin site instance from the request namespace. """
        request = self.request_factory.get("/owner-admin/")
        request.user = type(
            "OwnerUser",
            (),
            {
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "has_module_perms": lambda self, app_label: True,
                "has_perm": lambda self, perm: True,
            },
        )()
        request.resolver_match = type("ResolverMatch", (), {"namespace": owner_admin_site.name})()

        self.assertEqual(AdminSiteUnfoldCallbacks.site_title(request), owner_admin_site.get_site_title(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.site_header(request), owner_admin_site.get_site_header(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.site_symbol(request), owner_admin_site.get_site_symbol(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.site_url(request), owner_admin_site.get_site_url(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.site_dropdown(request), owner_admin_site.get_site_dropdown(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.show_search(request), owner_admin_site.get_show_sidebar_search(request))
        self.assertEqual(
            AdminSiteUnfoldCallbacks.show_all_applications(request),
            owner_admin_site.get_show_all_applications(request),
        )
        callback_navigation = AdminSiteUnfoldCallbacks.sidebar_navigation(request)
        site_navigation = owner_admin_site.get_sidebar_navigation(request)

        self.assertEqual([group["title"] for group in callback_navigation], [group["title"] for group in site_navigation])
        self.assertEqual(
            [item["title"] for group in callback_navigation for item in group["items"]],
            [item["title"] for group in site_navigation for item in group["items"]],
        )
        self.assertEqual(
            [item["link"] for group in callback_navigation for item in group["items"]],
            [item["link"] for group in site_navigation for item in group["items"]],
        )
        self.assertEqual(AdminSiteUnfoldCallbacks.scripts(request), owner_admin_site.get_scripts(request))
        self.assertEqual(AdminSiteUnfoldCallbacks.styles(request), owner_admin_site.get_styles(request))

    def test_owner_admin_site_metadata_prefers_the_active_tenant(self) -> None:
        """ Verify the owner admin metadata uses the active tenant when one is available. """
        request = self.request_factory.get("/owner-admin/")
        request.tenant = TenantModel(name="GEA Lubricantes", slug="gea-lubricantes")

        self.assertEqual("GEA Lubricantes", owner_admin_site.get_site_title(request))

    def test_master_admin_sidebar_navigation_includes_users_groups_and_tenancy(self) -> None:
        """ Verify the master admin sidebar includes account and tenancy management links. """
        request = self.request_factory.get("/admin/")
        request.user = type(
            "SuperUser",
            (),
            {
                "is_active": True,
                "is_superuser": True,
                "is_staff": True,
                "has_module_perms": lambda self, app_label: True,
                "has_perm": lambda self, perm: True,
            },
        )()
        navigation = master_admin_site.get_sidebar_navigation(request)

        item_links = {
            item["link"]
            for group in navigation
            for item in group["items"]
        }

        self.assertIn("/admin/accounts/usermodel/", item_links)
        self.assertIn("/admin/auth/group/", item_links)
        self.assertIn("/admin/tenancy/tenantmodel/", item_links)
        self.assertIn("/admin/tenancy/tenantgroupmodel/", item_links)
        self.assertIn("/admin/tenancy/tenantmembershipmodel/", item_links)
