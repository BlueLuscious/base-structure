""" Form used by the owner group admin. """

from django import forms
from django.contrib.auth.models import Group


class OwnerGroupAdminForm(forms.ModelForm):
    """ Owner-facing form for tenant-scoped support groups. """

    class Meta:
        """ Declarative field presentation for owner group editing. """

        model = Group
        fields = ("name", "permissions")
        labels = {
            "name": "Group name",
            "permissions": "Delegated permissions",
        }
        help_texts = {
            "name": "Use a clear name that reflects the support role for this tenant.",
            "permissions": "Only permissions that you already hold can be delegated.",
        }
