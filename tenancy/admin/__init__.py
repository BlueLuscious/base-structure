""" Tenancy admin package. """

from tenancy.admin.master import TenantGroupModelAdmin, TenantMembershipModelAdmin, TenantModelAdmin

__all__: list[str] = ["TenantMembershipModelAdmin", "TenantGroupModelAdmin", "TenantModelAdmin"]
