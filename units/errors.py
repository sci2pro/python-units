# -*- coding: utf-8 -*-
"""Domain exceptions for the units package."""


class UnitsError(Exception):
    """Base exception for unit-related failures."""


class InvalidValueError(UnitsError):
    """Raised when a numeric value is invalid for a Unit."""


class InvalidUnitError(UnitsError):
    """Raised when a provided unit object or unit definition is invalid."""


class UnitCompatibilityError(UnitsError):
    """Raised when an operation requires compatible units but they differ."""


class UnitOperandError(UnitsError):
    """Raised when an operation is attempted with an unsupported operand."""
