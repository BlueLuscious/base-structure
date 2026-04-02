""" Form used by the owner user admin tenant membership inline. """

from django import forms
from tenancy.choices import TenantRole
from tenancy.models import TenantMembershipModel


class TenantMembershipInlineForm(forms.ModelForm):
    """ Owner-facing form for one tenant-scoped user membership. """

    class Meta:
        """ Declarative field presentation for owner membership editing. """

        model = TenantMembershipModel
        fields = ("role", "is_active")
        labels = {
            "role": "Tenant role",
            "is_active": "Membership active",
        }
        help_texts = {
            "role": "Choose whether this person manages the tenant or works as staff for it.",
            "is_active": "Disable the tenant membership without deleting the user account.",
        }

    def __init__(self, *args, **kwargs) -> None:
        """ Limit editable tenant roles to owner-managed options.

        Args:
            *args: Positional form arguments.
            **kwargs: Keyword form arguments.
        """
        super().__init__(*args, **kwargs)
        
        role_field = self.fields.get("role")
        if role_field is not None:
            role_field.initial = TenantRole.EMPLOYEE
            role_field.choices = [
                (TenantRole.OWNER, TenantRole.OWNER.label),
                (TenantRole.EMPLOYEE, TenantRole.EMPLOYEE.label),
            ]

        is_active_field = self.fields.get("is_active")
        if is_active_field is not None:
            is_active_field.initial = True
