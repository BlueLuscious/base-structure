"""Helpers for tenant-aware media object paths."""

from tenancy.runtime import ActiveTenantContext


class TenantMediaPathBuilder:
    """Build tenant-aware media paths from the current runtime tenant context."""

    context_class = ActiveTenantContext

    @classmethod
    def build_current_tenant_media_prefix(cls) -> str:
        """Build the media prefix for the active tenant.

        Returns:
            str: Tenant-specific media prefix.

        Raises:
            RuntimeError: When tenant-aware media is used without an active tenant.
        """
        tenant = cls.context_class.get()
        if tenant is None:
            raise RuntimeError("Tenant-aware media storage requires an active tenant.")

        tenant_key = tenant.slug.strip()
        return f"tenants/{tenant_key}"

    @classmethod
    def build_tenant_media_name(cls, name: str) -> str:
        """Build one tenant-aware media object name.

        Args:
            name: Relative media object name produced by the caller.

        Returns:
            str: Tenant-aware media object name.
        """
        normalized_name = name.lstrip("/")
        tenant_prefix = cls.build_current_tenant_media_prefix()

        if normalized_name.startswith(f"{tenant_prefix}/"):
            return normalized_name

        return f"{tenant_prefix}/{normalized_name}"
