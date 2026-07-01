""" Typed parsing for project environment variables. """

import os
from math import isfinite
from django.core.exceptions import ImproperlyConfigured


class EnvironmentValueParser:
    """ Parse environment values with consistent, actionable errors. """

    TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
    FALSE_VALUES = frozenset({"0", "false", "no", "off"})

    @classmethod
    def get_bool(cls, name: str, default: bool) -> bool:
        """ Read a strict boolean environment variable.

        Args:
            name: Environment variable name.
            default: Value returned when the variable is not defined.

        Returns:
            bool: Parsed environment value.

        Raises:
            ImproperlyConfigured: When the value is not a supported boolean.
        """
        raw_value = os.environ.get(name)
        if raw_value is None:
            return default

        normalized_value = raw_value.strip().lower()
        if normalized_value in cls.TRUE_VALUES:
            return True
        if normalized_value in cls.FALSE_VALUES:
            return False

        raise ImproperlyConfigured(
            f"{name} must be one of: 1, true, yes, on, 0, false, no, off; "
            f"received {raw_value!r}."
        )

    @staticmethod
    def get_int(name: str, default: int) -> int:
        """ Read an integer environment variable.

        Args:
            name: Environment variable name.
            default: Value returned when the variable is not defined.

        Returns:
            int: Parsed environment value.

        Raises:
            ImproperlyConfigured: When the value is not a valid integer.
        """
        raw_value = os.environ.get(name)
        if raw_value is None:
            return default

        try:
            return int(raw_value)
        except ValueError as error:
            raise ImproperlyConfigured(
                f"{name} must be an integer; received {raw_value!r}."
            ) from error

    @staticmethod
    def get_positive_float(name: str, default: float) -> float:
        """ Read a positive floating-point environment variable.

        Args:
            name: Environment variable name.
            default: Value returned when the variable is not defined.

        Returns:
            float: Parsed positive environment value.

        Raises:
            ImproperlyConfigured: When the value is not a positive number.
        """
        raw_value = os.environ.get(name)
        if raw_value is None:
            return default

        try:
            parsed_value = float(raw_value)
        except ValueError as error:
            raise ImproperlyConfigured(
                f"{name} must be a positive number; received {raw_value!r}."
            ) from error

        if not isfinite(parsed_value) or parsed_value <= 0:
            raise ImproperlyConfigured(
                f"{name} must be a finite number greater than zero; received {raw_value!r}."
            )
        return parsed_value
