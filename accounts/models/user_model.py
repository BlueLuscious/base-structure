""" Custom user model for the accounts app. """

from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models.managers.user_model_manager import UserModelManager

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
    from tenancy.models.querysets import TenantMembershipModelQuerySet, TenantModelQuerySet


class UserModel(AbstractUser):
    """ Base user model used by Django auth within this project. """

    tenants: "RelatedManager[TenantModelQuerySet]" = models.ManyToManyField(
        "tenancy.TenantModel",
        through="tenancy.TenantMembershipModel",
        related_name="users",
        blank=True,
    )
    objects: UserModelManager = UserModelManager()

    tenant_memberships: "RelatedManager[TenantMembershipModelQuerySet]"
