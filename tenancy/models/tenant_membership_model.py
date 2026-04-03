""" Tenant membership persistence model. """

from typing import TYPE_CHECKING
from uuid import UUID
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from tenancy.choices import TenantRole
from tenancy.models.managers.tenant_membership_model_manager import TenantMembershipModelManager

if TYPE_CHECKING:
    from accounts.models import UserModel
    from tenancy.models import TenantModel


class TenantMembershipModel(models.Model):
    """ Membership linking one user to one tenant with a scoped role. """

    tenant: "TenantModel" = models.ForeignKey(
        "tenancy.TenantModel",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user: "UserModel" = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
    )
    role = models.CharField(max_length=16, choices=TenantRole.choices, default=TenantRole.OWNER)
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: TenantMembershipModelManager = TenantMembershipModelManager()

    id: int
    user_id: int
    tenant_id: UUID

    class Meta:
        ordering = ("tenant__name", "user__username", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("tenant", "user"),
                name="tenant_membership_unique_tenant_user",
            ),
            models.UniqueConstraint(
                fields=("user",),
                condition=Q(is_primary=True),
                name="tenant_membership_unique_primary_per_user",
            ),
        ]
        verbose_name = _("Business access")
        verbose_name_plural = _("Business access")

    def __str__(self) -> str:
        """ Return the admin-friendly tenant membership label.

        Returns:
            str: Membership label.
        """
        return f"{self.user} -> {self.tenant} ({self.role})"
