""" Role choices for tenant memberships. """

from django.db import models


class TenantRole(models.TextChoices):
    """ Reusable roles describing a user's relationship with a tenant. """

    MASTER = "master", "Master"
    OWNER = "owner", "Owner"
    EMPLOYEE = "employee", "Employee"
