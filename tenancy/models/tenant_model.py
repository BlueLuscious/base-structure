""" Tenant persistence model. """

from typing import TYPE_CHECKING
from uuid import uuid4
from django.db import models
from tenancy.models.managers.tenant_model_manager import TenantModelManager

if TYPE_CHECKING:
    from accounts.models.managers.user_model_manager import UserModelManager
    from tenancy.models.managers.tenant_membership_model_manager import TenantMembershipModelManager


class TenantModel(models.Model):
    """ Root tenant entity used to scope business data across the project. """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: TenantModelManager = TenantModelManager()

    memberships: "TenantMembershipModelManager"
    users: "UserModelManager"

    class Meta:
        ordering = ("name",)
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self) -> str:
        """ Return the admin-friendly tenant label.

        Returns:
            str: Tenant name.
        """
        return self.name
