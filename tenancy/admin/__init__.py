"""Tenancy admin package."""

from tenancy.admin.master import (
    TenantBrandingModelAdmin,
    TenantGroupModelAdmin,
    TenantMembershipModelAdmin,
    TenantModelAdmin,
)
from tenancy.admin.owner import (
    OwnerTenantSettingsAdmin,
    OwnerTenantSettingsForm,
    TenantBrandingInline,
    TenantBrandingInlineForm,
    TenantBrandingInlineFormSet,
)

__all__: list[str] = [
    "OwnerTenantSettingsAdmin",
    "OwnerTenantSettingsForm",
    "TenantBrandingInline",
    "TenantBrandingInlineForm",
    "TenantBrandingInlineFormSet",
    "TenantBrandingModelAdmin",
    "TenantMembershipModelAdmin",
    "TenantGroupModelAdmin",
    "TenantModelAdmin",
]
