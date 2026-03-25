""" Registry of admin site import paths per namespace. """

from core.adminsites.admin_namespace import AdminNamespace


ADMIN_SITE_REGISTRY: dict[AdminNamespace, str] = {
    AdminNamespace.MASTER: "core.adminsites.sites.master_admin_site.MasterAdminSite",
    AdminNamespace.OWNER: "core.adminsites.sites.owner_admin_site.OwnerAdminSite",
}
