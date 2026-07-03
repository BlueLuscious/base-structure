"""Validation for relationships between environment-driven settings."""

from django.core.exceptions import ImproperlyConfigured


class EnvironmentContractValidator:
    """Validate environment values that must agree with each other."""

    @staticmethod
    def validate_mutually_exclusive(
        first_name: str,
        first_enabled: bool,
        second_name: str,
        second_enabled: bool,
    ) -> None:
        """Reject two settings that cannot be enabled together.

        Args:
            first_name: Name of the first environment variable.
            first_enabled: Whether the first setting is enabled.
            second_name: Name of the second environment variable.
            second_enabled: Whether the second setting is enabled.

        Raises:
            ImproperlyConfigured: When both settings are enabled.
        """
        if first_enabled and second_enabled:
            raise ImproperlyConfigured(f"{first_name} and {second_name} cannot both be enabled.")
