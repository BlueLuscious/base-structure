""" Owner-facing tenant settings form. """

from django import forms
from tenancy.models import TenantModel


class OwnerTenantSettingsForm(forms.ModelForm):
    """ Minimal tenant form used by the owner business settings screen. """

    class Meta:
        """ Declarative configuration for the tenant settings form. """

        model = TenantModel
        fields: tuple[str, ...] = ()
