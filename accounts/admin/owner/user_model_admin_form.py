""" Form used by the owner user admin change view. """

from unfold.forms import UserChangeForm
from accounts.models import UserModel


class OwnerUserModelAdminForm(UserChangeForm):
    """ Owner-facing form for editing support user accounts. """

    class Meta(UserChangeForm.Meta):
        """ Declarative field presentation for owner user editing. """

        model = UserModel
        fields = ("username", "first_name", "last_name", "email", "is_active", "is_staff", "groups")
        labels = {
            "username": "Username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
            "is_active": "Active",
            "is_staff": "Can access owner admin",
            "groups": "Groups",
        }
        help_texts = {
            "email": "Use a real contact address for support and password recovery.",
            "is_active": "Disable this user instead of deleting the account.",
            "is_staff": "Keep this enabled so the user can access the owner administration site.",
            "groups": "Only groups that belong to the active tenant can be assigned here.",
        }
