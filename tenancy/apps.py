""" App configuration for the tenancy domain. """

from django.apps import AppConfig


class TenancyConfig(AppConfig):
    """ Django app configuration for tenant-related persistence. """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tenancy"
