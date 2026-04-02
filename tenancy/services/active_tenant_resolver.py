""" Service for resolving the active tenant for one request. """

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from tenancy.models import TenantMembershipModel, TenantModel
from tenancy.session import ActiveTenantSessionStore


class ActiveTenantResolver:
    """ Resolve the active tenant for one request using memberships and session state. """

    session_store_class = ActiveTenantSessionStore

    @classmethod
    def resolve(cls, request: HttpRequest) -> TenantModel | None:
        """ Resolve the active tenant for the current request.

        Resolution order:
        1. Active tenant stored in session, when the user still belongs to it.
        2. Primary active tenant membership for the authenticated user.
        3. First active tenant membership for the authenticated user.

        Args:
            request: Current HTTP request.

        Returns:
            TenantModel | None: Resolved active tenant or ``None``.
        """
        user = request.user

        if isinstance(user, AnonymousUser) or not getattr(user, "is_authenticated", False):
            cls.session_store_class.clear(request)
            return None

        active_memberships = (
            TenantMembershipModel.objects.for_user_active_tenants(user)
            .with_tenant()
            .ordered_for_active_tenant_resolution()
        )

        session_tenant_id = cls.session_store_class.get_tenant_id(request)

        if session_tenant_id:
            session_membership = active_memberships.filter(tenant_id=session_tenant_id).first()
            if session_membership is not None:
                return session_membership.tenant

        resolved_membership = active_memberships.first()

        if resolved_membership is None:
            cls.session_store_class.clear(request)
            return None

        cls.session_store_class.set_tenant(request, resolved_membership.tenant)
        return resolved_membership.tenant
