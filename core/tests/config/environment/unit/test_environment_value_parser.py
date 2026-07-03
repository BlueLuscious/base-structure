"""Tests for strict environment value parsing."""

import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured

from core.config.environment import EnvironmentValueParser
from core.testing import LoggedSimpleTestCase


class TestEnvironmentValueParser(LoggedSimpleTestCase):
    """Verify environment values are parsed through an explicit contract."""

    def test_bool_uses_default_when_variable_is_missing(self) -> None:
        """Verify missing boolean variables preserve the supplied default."""
        with patch.dict(os.environ, {}, clear=True):
            result = EnvironmentValueParser.get_bool("FEATURE_ENABLED", True)

        self.assertIs(result, True)

    def test_bool_accepts_documented_true_and_false_values(self) -> None:
        """Verify documented boolean spellings are parsed case-insensitively."""
        with patch.dict(
            os.environ,
            {"TRUE_VALUE": " YES ", "FALSE_VALUE": "Off"},
            clear=True,
        ):
            true_result = EnvironmentValueParser.get_bool("TRUE_VALUE", False)
            false_result = EnvironmentValueParser.get_bool("FALSE_VALUE", True)

        self.assertIs(true_result, True)
        self.assertIs(false_result, False)

    def test_bool_rejects_unsupported_values_with_variable_name(self) -> None:
        """Verify invalid booleans identify the broken environment variable."""
        with patch.dict(os.environ, {"FEATURE_ENABLED": "sometimes"}, clear=True):
            with self.assertRaisesMessage(ImproperlyConfigured, "FEATURE_ENABLED"):
                EnvironmentValueParser.get_bool("FEATURE_ENABLED", False)

    def test_int_rejects_invalid_values_with_variable_name(self) -> None:
        """Verify invalid integers identify the broken environment variable."""
        with patch.dict(os.environ, {"EMAIL_PORT": "smtp"}, clear=True):
            with self.assertRaisesMessage(ImproperlyConfigured, "EMAIL_PORT"):
                EnvironmentValueParser.get_int("EMAIL_PORT", 1025)

    def test_positive_float_accepts_positive_values(self) -> None:
        """Verify positive decimal values support integration-test timing."""
        with patch.dict(os.environ, {"POLL_INTERVAL": "0.25"}, clear=True):
            result = EnvironmentValueParser.get_positive_float("POLL_INTERVAL", 1.0)

        self.assertEqual(0.25, result)

    def test_positive_float_rejects_non_positive_and_non_finite_values(self) -> None:
        """Verify timing values must be finite and greater than zero."""
        for invalid_value in ("0", "-1", "nan", "inf"):
            with self.subTest(invalid_value=invalid_value):
                with patch.dict(
                    os.environ,
                    {"POLL_INTERVAL": invalid_value},
                    clear=True,
                ):
                    with self.assertRaisesMessage(
                        ImproperlyConfigured,
                        "POLL_INTERVAL",
                    ):
                        EnvironmentValueParser.get_positive_float(
                            "POLL_INTERVAL",
                            1.0,
                        )
