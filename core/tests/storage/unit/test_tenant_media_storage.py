""" Unit tests for tenant-aware media storage helpers. """

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.core.files.base import ContentFile
from core.config.storage import MediaStorageAdapterResolver
from core.config.storage.media_storage.backends.tenant_file_system_storage import TenantFileSystemStorage
from core.config.storage.media_storage.paths.tenant_media_path_builder import TenantMediaPathBuilder
from core.tenancy import ActiveTenantContext
from core.testing.base import LoggedSimpleTestCase
from tenancy.models import TenantModel


class TestTenantMediaStorage(LoggedSimpleTestCase):
    """ Verify media storage prefixes uploaded files with the active tenant. """

    base_dir: Path

    @classmethod
    def setUpClass(cls) -> None:
        """ Prepare a stable base directory for storage adapter resolution. """
        super().setUpClass()
        cls.base_dir = Path(__file__).resolve().parents[4]

    def test_build_tenant_media_name_keeps_names_unchanged_without_an_active_tenant(self) -> None:
        """ Verify media object names stay untouched when no tenant context exists. """
        self.assertEqual("products/image.png", TenantMediaPathBuilder.build_tenant_media_name("products/image.png"))

    def test_build_tenant_media_name_prefixes_names_with_the_active_tenant_slug(self) -> None:
        """ Verify media object names gain the active tenant folder when a tenant is present. """
        tenant = TenantModel(name="GEA Center", slug="gea-center")
        tenant_token = ActiveTenantContext.set(tenant)

        try:
            self.assertEqual(
                "tenants/gea-center/products/image.png",
                TenantMediaPathBuilder.build_tenant_media_name("products/image.png"),
            )
        finally:
            ActiveTenantContext.reset(tenant_token)

    def test_tenant_file_system_storage_saves_files_inside_the_active_tenant_folder(self) -> None:
        """ Verify the local tenant-aware backend saves files inside the active tenant directory. """
        tenant = TenantModel(name="GEA Center", slug="gea-center")
        tenant_token = ActiveTenantContext.set(tenant)

        try:
            with TemporaryDirectory() as media_root:
                storage = TenantFileSystemStorage(location=media_root, base_url="/media/")
                stored_name = storage.save("products/image.txt", ContentFile(b"hello"))

                self.assertEqual("tenants/gea-center/products/image.txt", stored_name)
                self.assertTrue(Path(media_root, stored_name).exists())
        finally:
            ActiveTenantContext.reset(tenant_token)

    def test_media_storage_resolver_build_config_uses_the_tenant_aware_local_backend(self) -> None:
        """ Verify local media configuration now uses the tenant-aware filesystem backend. """
        environment = {
            "MEDIAFILES_PROVIDER": "local",
            "MEDIA_URL": "/media/",
            "MEDIA_ROOT": "media",
        }

        with patch.dict(os.environ, environment, clear=False):
            storage_config = MediaStorageAdapterResolver.build_config(self.base_dir)

        self.assertEqual(
            "core.config.storage.media_storage.backends.tenant_file_system_storage.TenantFileSystemStorage",
            storage_config.storages["default"]["BACKEND"],
        )
