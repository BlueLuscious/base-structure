""" Model tests for tenant persistence. """

from uuid import UUID
from core.testing.base import LoggedTestCase
from tenancy.models import TenantModel


class TestTenantModel(LoggedTestCase):
    """ Verify tenant persistence and representation. """

    def test_string_representation_uses_tenant_name(self) -> None:
        """ Verify the tenant string representation stays human-friendly. """
        tenant = TenantModel.objects.create(name="GEA Center", slug="gea-center")

        self.assertEqual("GEA Center", str(tenant))
        self.assertIsInstance(tenant.pk, UUID)
