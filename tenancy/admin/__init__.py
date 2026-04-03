""" Tenancy admin package. """

from tenancy.admin.master import (
    TenantBrandingModelAdmin,
    TenantGroupModelAdmin,
    TenantMembershipModelAdmin,
    TenantModelAdmin,
)

__all__: list[str] = [
    "TenantBrandingModelAdmin",
    "TenantMembershipModelAdmin",
    "TenantGroupModelAdmin",
    "TenantModelAdmin",
]
