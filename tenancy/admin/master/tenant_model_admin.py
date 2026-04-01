""" Tenant admin registration for the master admin site. """

from django.contrib import admin
from unfold.admin import ModelAdmin
from core.adminsites.site_instances import master_admin_site
from tenancy.models import TenantModel


@admin.register(TenantModel, site=master_admin_site)
class TenantModelAdmin(ModelAdmin):
    """ Unfold-compatible tenant admin for the master admin site. """

    list_display = ("name", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
