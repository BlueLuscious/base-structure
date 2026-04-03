""" Access policy helpers for tenant-scoped accounts administration. """

from typing import TYPE_CHECKING
from django.apps import apps
from django.http import HttpRequest
from tenancy.choices import TenantRole
from tenancy.access.tenant_access_policy import TenantAccessPolicy

if TYPE_CHECKING:
    from django.contrib.auth.models import Group
    from accounts.models import UserModel


class TenantAccountsAccessPolicy:
    """ Resolve access to owner-managed users and groups inside one tenant. """

    visible_user_roles = (TenantRole.OWNER, TenantRole.OPERATOR)

    @classmethod
    def can_manage_accounts(cls, request: HttpRequest) -> bool:
        """ Return whether the current request may manage tenant-scoped accounts.

        Args:
            request: Current HTTP request.

        Returns:
            bool: ``True`` when the request user may manage owner accounts in the active tenant.
        """
        return TenantAccessPolicy.can_manage_tenant(request.user, getattr(request, "tenant", None))

    @classmethod
    def can_view_user(cls, request: HttpRequest, user: "UserModel") -> bool:
        """ Return whether one target user should be visible in owner accounts admin.

        Args:
            request: Current HTTP request.
            user: User being inspected.

        Returns:
            bool: ``True`` when the user belongs to the active tenant in one visible role.
        """
        tenant = getattr(request, "tenant", None)
        if tenant is None or getattr(user, "is_superuser", False):
            return False

        return user.tenant_memberships.filter(
            tenant=tenant,
            role__in=cls.visible_user_roles,
        ).exists()

    @classmethod
    def can_view_group(cls, request: HttpRequest, group: "Group") -> bool:
        """ Return whether one target group should be visible in owner accounts admin.

        Args:
            request: Current HTTP request.
            group: Group being inspected.

        Returns:
            bool: ``True`` when the group belongs to the active tenant and the actor may manage accounts.
        """
        tenant = getattr(request, "tenant", None)
        if tenant is None or not cls.can_manage_accounts(request):
            return False

        return apps.get_model("tenancy", "TenantGroupModel").objects.filter(tenant=tenant, group=group).exists()
