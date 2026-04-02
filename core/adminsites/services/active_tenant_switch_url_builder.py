""" Service for building active-tenant switch URLs. """

from typing import TYPE_CHECKING
from django.http import HttpRequest
from django.urls import reverse
from django.utils.http import urlencode

if TYPE_CHECKING:
    from tenancy.models import TenantModel


class ActiveTenantSwitchUrlBuilder:
    """ Build safe active-tenant switch URLs for the current request context. """

    @classmethod
    def build(cls, request: HttpRequest, tenant: "TenantModel") -> str:
        """ Build one tenant switch URL including the current request as safe return target.

        Args:
            request: Current admin request.
            tenant: Tenant that should become active after the switch.

        Returns:
            str: Absolute application URL for the active-tenant switch flow.
        """
        next_path = request.get_full_path()
        return (
            f"{reverse('switch-active-tenant', kwargs={'tenant_id': tenant.pk})}"
            f"?{urlencode({'next': next_path})}"
        )
