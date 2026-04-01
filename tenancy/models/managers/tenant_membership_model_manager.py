""" Custom manager for the tenant membership model. """

from typing import TYPE_CHECKING
from django.db import models
from tenancy.models.querysets.tenant_membership_model_queryset import TenantMembershipModelQuerySet

if TYPE_CHECKING:
    from accounts.models import UserModel
    from tenancy.models import TenantMembershipModel, TenantModel


class TenantMembershipModelManager(models.Manager["TenantMembershipModel"]):
    """ Manager exposing typed tenant membership queryset helpers. """

    def get_queryset(self) -> TenantMembershipModelQuerySet:
        """ Return the base queryset for tenant membership queries.

        Returns:
            TenantMembershipModelQuerySet: Specialized queryset for TenantMembershipModel.
        """
        return TenantMembershipModelQuerySet(self.model, using=self._db)

    def active(self) -> TenantMembershipModelQuerySet:
        """ Return active memberships only.

        Returns:
            TenantMembershipModelQuerySet: Active memberships.
        """
        return self.get_queryset().active()

    def for_user(self, user: "UserModel") -> TenantMembershipModelQuerySet:
        """ Return memberships related to one user.

        Args:
            user: User whose memberships should be returned.

        Returns:
            TenantMembershipModelQuerySet: Memberships linked to the provided user.
        """
        return self.get_queryset().for_user(user)

    def for_tenant(self, tenant: "TenantModel") -> TenantMembershipModelQuerySet:
        """ Return memberships related to one tenant.

        Args:
            tenant: Tenant whose memberships should be returned.

        Returns:
            TenantMembershipModelQuerySet: Memberships linked to the provided tenant.
        """
        return self.get_queryset().for_tenant(tenant)

    def primary(self) -> TenantMembershipModelQuerySet:
        """ Return primary memberships only.

        Returns:
            TenantMembershipModelQuerySet: Primary memberships.
        """
        return self.get_queryset().primary()

    def owners(self) -> TenantMembershipModelQuerySet:
        """ Return owner memberships only.

        Returns:
            TenantMembershipModelQuerySet: Owner memberships.
        """
        return self.get_queryset().owners()
