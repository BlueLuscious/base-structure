""" Group admin registration for the owner admin site. """

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from accounts.admin.owner.group_admin_form import OwnerGroupAdminForm
from accounts.services.owner_delegable_permission_resolver import OwnerDelegablePermissionResolver
from core.adminsites.site_instances import owner_admin_site
from tenancy.models import TenantGroupModel
from tenancy.access.tenant_accounts_access_policy import TenantAccountsAccessPolicy


@admin.register(Group, site=owner_admin_site)
class OwnerGroupAdmin(BaseGroupAdmin, ModelAdmin):
    """ Guided group admin scoped to the active tenant. """

    class Media:
        """ Owner admin assets for small layout refinements. """

        css = {
            "all": ("accounts/admin/owner/group_admin.css",),
        }

    form = OwnerGroupAdminForm
    save_on_top = True
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        (
            "Group details",
            {
                "classes": ("tab",),
                "description": "Create and maintain support groups for the active tenant.",
                "fields": ("name",),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("tab",),
                "description": "Delegate only the permissions already held by the current owner.",
                "fields": ("permissions",),
            },
        ),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Group]:
        """ Return only groups bound to the active tenant.

        Args:
            request: Current admin request.

        Returns:
            QuerySet[Group]: Tenant-scoped owner-visible groups.
        """
        tenant = getattr(request, "tenant", None)
        queryset = super().get_queryset(request)

        if tenant is None:
            return queryset.none()

        return queryset.filter(tenant_binding__tenant=tenant)

    def formfield_for_manytomany(self, db_field, request: HttpRequest, **kwargs):
        """ Filter delegated permissions to the current owner's effective permissions.

        Args:
            db_field: Django model field being converted into a form field.
            request: Current admin request.
            **kwargs: Remaining field construction arguments.

        Returns:
            forms.Field: Built admin form field.
        """
        if db_field.name == "permissions":
            kwargs["queryset"] = OwnerDelegablePermissionResolver.get_queryset(
                request.user,
                getattr(request, "tenant", None),
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request: HttpRequest, obj: Group, form: OwnerGroupAdminForm, change: bool) -> None:
        """ Persist one tenant-scoped group and create its tenant binding on add.

        Args:
            request: Current admin request.
            obj: Group being saved.
            form: Bound owner group form.
            change: Whether this is an existing group edit.
        """
        super().save_model(request, obj, form, change)

        if change:
            return

        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return

        TenantGroupModel.objects.get_or_create(tenant=tenant, group=obj)

    def has_module_permission(self, request: HttpRequest) -> bool:
        """ Require an active tenant before exposing the owner group module.

        Args:
            request: Current admin request.

        Returns:
            bool: True when the request has an active tenant and base permissions.
        """
        return TenantAccountsAccessPolicy.can_manage_accounts(request) and super().has_module_permission(request)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """ Require an active tenant before allowing group creation.

        Args:
            request: Current admin request.

        Returns:
            bool: True when the request has an active tenant and base permissions.
        """
        return TenantAccountsAccessPolicy.can_manage_accounts(request) and super().has_add_permission(request)

    def has_view_permission(self, request: HttpRequest, obj: Group | None = None) -> bool:
        """ Restrict group visibility to the active tenant scope.

        Args:
            request: Current admin request.
            obj: Group being inspected, when present.

        Returns:
            bool: True when the group belongs to the active tenant and base permissions pass.
        """
        if not TenantAccountsAccessPolicy.can_manage_accounts(request):
            return False

        if not super().has_view_permission(request, obj):
            return False

        if obj is None:
            return True

        return TenantAccountsAccessPolicy.can_view_group(request, obj)

    def has_change_permission(self, request: HttpRequest, obj: Group | None = None) -> bool:
        """ Restrict group editing to the active tenant scope.

        Args:
            request: Current admin request.
            obj: Group being edited, when present.

        Returns:
            bool: True when the group belongs to the active tenant and base permissions pass.
        """
        if not TenantAccountsAccessPolicy.can_manage_accounts(request):
            return False

        if not super().has_change_permission(request, obj):
            return False

        if obj is None:
            return True

        return TenantAccountsAccessPolicy.can_view_group(request, obj)

    def has_delete_permission(self, request: HttpRequest, obj: Group | None = None) -> bool:
        """ Restrict group deletion to the active tenant scope.

        Args:
            request: Current admin request.
            obj: Group being deleted, when present.

        Returns:
            bool: True when the group belongs to the active tenant and base permissions pass.
        """
        if not TenantAccountsAccessPolicy.can_manage_accounts(request):
            return False

        if not super().has_delete_permission(request, obj):
            return False

        if obj is None:
            return True

        return TenantAccountsAccessPolicy.can_view_group(request, obj)
