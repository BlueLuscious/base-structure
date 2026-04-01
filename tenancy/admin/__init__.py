""" Tenancy admin package. """

from tenancy.admin.master import TenantMembershipModelAdmin, TenantModelAdmin

__all__: list[str] = ["TenantMembershipModelAdmin", "TenantModelAdmin"]
