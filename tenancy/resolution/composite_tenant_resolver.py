""" Composite active-tenant resolver built from small strategies. """

from typing import TYPE_CHECKING
from django.http import HttpRequest
from tenancy.models import TenantModel

if TYPE_CHECKING:
    from tenancy.resolution.strategies.tenant_resolution_strategy import TenantResolutionStrategy


class CompositeTenantResolver:
    """ Resolve one tenant by trying small strategies in order. """

    strategies: tuple[type["TenantResolutionStrategy"], ...] = ()

    @classmethod
    def resolve(cls, request: HttpRequest) -> TenantModel | None:
        """ Return the first tenant resolved by the configured strategies.

        Args:
            request: Current HTTP request.

        Returns:
            TenantModel | None: First resolved tenant or ``None`` when no strategy matches.
        """
        for strategy_class in cls.strategies:
            tenant = strategy_class.resolve(request)
            if tenant is not None:
                return tenant

        return None
