"""Tests for relationships between environment settings."""

from django.core.exceptions import ImproperlyConfigured

from core.config.environment import EnvironmentContractValidator
from core.testing import LoggedSimpleTestCase


class TestEnvironmentContractValidator(LoggedSimpleTestCase):
    """Verify related settings cannot form unsupported combinations."""

    def test_mutually_exclusive_values_allow_at_most_one_enabled_setting(self) -> None:
        """Verify zero or one enabled value satisfies the contract."""
        valid_combinations = ((False, False), (True, False), (False, True))

        for first_enabled, second_enabled in valid_combinations:
            with self.subTest(
                first_enabled=first_enabled,
                second_enabled=second_enabled,
            ):
                EnvironmentContractValidator.validate_mutually_exclusive(
                    "EMAIL_USE_TLS",
                    first_enabled,
                    "EMAIL_USE_SSL",
                    second_enabled,
                )

    def test_mutually_exclusive_values_reject_both_enabled_settings(self) -> None:
        """Verify the error identifies both conflicting settings."""
        expected_message = "EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be enabled."

        with self.assertRaisesMessage(ImproperlyConfigured, expected_message):
            EnvironmentContractValidator.validate_mutually_exclusive(
                "EMAIL_USE_TLS",
                True,
                "EMAIL_USE_SSL",
                True,
            )
