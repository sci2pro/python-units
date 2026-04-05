# -*- coding: utf-8 -*-
"""Numeric helper utilities."""

from __future__ import annotations

from numbers import Number, Real
from typing import TypeAlias

from core.errors import InvalidValueError

Scalar: TypeAlias = int | float | complex


def is_number(value: object) -> bool:
    """Return ``True`` when ``value`` is a supported numeric scalar."""
    return isinstance(value, Number) and not isinstance(value, bool)


def is_real_number(value: object) -> bool:
    """Return ``True`` when ``value`` is a supported real numeric scalar."""
    return isinstance(value, Real) and not isinstance(value, bool)


def validate_numeric_value(value: object) -> None:
    """Raise when ``value`` is not a supported numeric scalar."""
    if not is_number(value):
        raise InvalidValueError(
            "value must be a numeric scalar, got {}".format(type(value).__name__)
        )
