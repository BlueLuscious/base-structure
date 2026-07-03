"""Accounts admin package."""

from accounts.admin.master import GroupAdmin, UserModelAdmin
from accounts.admin.owner import OwnerGroupAdmin, OwnerUserModelAdmin

__all__: list[str] = ["GroupAdmin", "OwnerGroupAdmin", "OwnerUserModelAdmin", "UserModelAdmin"]
