""" Custom user model for the accounts app. """

from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models.managers.user_model_manager import UserModelManager

if TYPE_CHECKING:
    from tenancy.models.managers import TenantMembershipModelManager, TenantModelManager


class UserModel(AbstractUser):
    """ Base user model used by Django auth within this project. """

    tenants = models.ManyToManyField(
        "tenancy.TenantModel",
        through="tenancy.TenantMembershipModel",
        related_name="users",
        blank=True,
    )
    objects: UserModelManager = UserModelManager()

    tenant_memberships: "TenantMembershipModelManager"
    tenants: "TenantModelManager"
