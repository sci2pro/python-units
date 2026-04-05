# -*- coding: utf-8 -*-
"""Quantity type and quantity operations."""

from __future__ import annotations

from numbers import Number, Real
from typing import TypeAlias

from .errors import InvalidValueError, UnitCompatibilityError, UnitOperandError
from .unit import BaseUnit, SIUnit, clone_unit

Scalar: TypeAlias = int | float | complex


def _is_number(value: object) -> bool:
    return isinstance(value, Number) and not isinstance(value, bool)


def _is_real_number(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


def _validate_numeric_value(value: object) -> None:
    if not _is_number(value):
        raise InvalidValueError('value must be a numeric scalar, got {}'.format(type(value).__name__))


def _require_quantity_operand(operand: object, operation: str) -> None:
    if not isinstance(operand, Quantity):
        raise UnitOperandError(
            'unsupported operand for {}: {}'.format(operation, type(operand).__name__)
        )


class Quantity(object):
    """A numeric value coupled to a unit definition.

    Args:
        value: Numeric magnitude of the quantity.
        unit: Unit definition for the quantity. ``None`` means dimensionless.

    Raises:
        InvalidValueError: If ``value`` is not numeric.
        InvalidUnitError: If ``unit`` is not a supported unit definition.
    """

    def __init__(self, value: Scalar, unit: BaseUnit | None = None) -> None:
        _validate_numeric_value(value)
        self._value = value
        self._unit = clone_unit(unit)

    @property
    def value(self) -> Scalar:
        """Return the numeric value for the quantity."""
        return self._value

    @value.setter
    def value(self, value: Scalar) -> None:
        _validate_numeric_value(value)
        self._value = value

    @property
    def unit(self) -> BaseUnit:
        """Return the unit definition for the quantity."""
        return self._unit

    @unit.setter
    def unit(self, unit: BaseUnit | None) -> None:
        self._unit = clone_unit(unit)

    @property
    def is_unitless(self) -> bool:
        """Return ``True`` when the quantity is dimensionless."""
        return all(exponent == 0 for exponent in self.unit.unit_dict.values())

    def _dimensionless_unit(self) -> SIUnit:
        return SIUnit()

    def _require_compatible_quantity(self, quantity2: object, operation: str) -> None:
        _require_quantity_operand(quantity2, operation)
        if self.unit != quantity2.unit:
            raise UnitCompatibilityError('units mismatch: {} and {}'.format(self.unit, quantity2.unit))

    def _require_real_scalar(self, value: object, operation: str) -> None:
        if not _is_real_number(value):
            raise UnitOperandError(
                'unsupported scalar for {}: {}'.format(operation, type(value).__name__)
            )

    def _require_numeric_scalar(self, value: object, operation: str) -> None:
        if not _is_number(value):
            raise UnitOperandError(
                'unsupported scalar for {}: {}'.format(operation, type(value).__name__)
            )

    @property
    def full_units(self) -> str:
        """Render derived units in their SI decomposition."""
        if not self.is_unitless and not isinstance(self.unit, SIUnit):
            return '{} {}'.format(self.value, self.unit.full_units).strip()
        return str(self)

    def __add__(self, quantity2: object) -> Quantity:
        self._require_compatible_quantity(quantity2, 'addition')
        return self.__class__(self.value + quantity2.value, self.unit)

    def __radd__(self, quantity2: object) -> Quantity:
        return self.__add__(quantity2)

    def __sub__(self, quantity2: object) -> Quantity:
        self._require_compatible_quantity(quantity2, 'subtraction')
        return self.__class__(self.value - quantity2.value, self.unit)

    def __rsub__(self, quantity2: object) -> Quantity:
        self._require_compatible_quantity(quantity2, 'subtraction')
        return self.__class__(quantity2.value - self.value, self.unit)

    def __mul__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value * quantity2.value, self.unit * quantity2.unit)
        self._require_numeric_scalar(quantity2, 'multiplication')
        return self.__class__(self.value * quantity2, self.unit)

    def __rmul__(self, quantity2: object) -> Quantity:
        return self.__mul__(quantity2)

    def __truediv__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value / quantity2.value, self.unit / quantity2.unit)
        self._require_numeric_scalar(quantity2, 'division')
        return self.__class__(self.value / quantity2, self.unit)

    def __rtruediv__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value / self.value, quantity2.unit / self.unit)
        self._require_numeric_scalar(quantity2, 'division')
        return self.__class__(quantity2 / self.value, self._dimensionless_unit() / self.unit)

    def __floordiv__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value // quantity2.value, self.unit / quantity2.unit)
        self._require_real_scalar(quantity2, 'floor division')
        return self.__class__(self.value // quantity2, self.unit)

    def __rfloordiv__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value // self.value, quantity2.unit / self.unit)
        self._require_real_scalar(quantity2, 'floor division')
        return self.__class__(quantity2 // self.value, self._dimensionless_unit() / self.unit)

    def __mod__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, 'modulo')
            return self.__class__(self.value % quantity2.value, self.unit)
        self._require_real_scalar(quantity2, 'modulo')
        return self.__class__(self.value % quantity2, self.unit)

    def __rmod__(self, quantity2: object) -> Quantity:
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, 'modulo')
            return self.__class__(quantity2.value % self.value, self.unit)
        self._require_real_scalar(quantity2, 'modulo')
        return self.__class__(quantity2 % self.value, self._dimensionless_unit() / self.unit)

    def __divmod__(self, quantity2: object) -> tuple[Quantity, Quantity]:
        return self.__floordiv__(quantity2), self.__mod__(quantity2)

    def __rdivmod__(self, quantity2: object) -> tuple[Quantity, Quantity]:
        return self.__rfloordiv__(quantity2), self.__rmod__(quantity2)

    def __neg__(self) -> Quantity:
        return self.__class__(-self.value, self.unit)

    def __pos__(self) -> Quantity:
        return self.__class__(+self.value, self.unit)

    def __abs__(self) -> Quantity:
        return self.__class__(abs(self.value), self.unit)

    def __complex__(self) -> complex:
        raise TypeError('invalid conversion from Quantity object to complex')

    def __int__(self) -> int:
        raise TypeError('invalid conversion from Quantity object to int')

    def __float__(self) -> float:
        raise TypeError('invalid conversion from Quantity object to float')

    def __str__(self) -> str:
        return '{} {}'.format(self.value, self.unit).strip()


def int_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to int while preserving its unit."""
    _require_quantity_operand(quantity, 'int conversion')
    return Quantity(int(quantity.value), quantity.unit)


def float_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to float while preserving its unit."""
    _require_quantity_operand(quantity, 'float conversion')
    return Quantity(float(quantity.value), quantity.unit)


def long_quantity(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``int_quantity``."""
    _require_quantity_operand(quantity, 'long conversion')
    return Quantity(int(quantity.value), quantity.unit)


def complex_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to complex while preserving its unit."""
    _require_quantity_operand(quantity, 'complex conversion')
    return Quantity(complex(quantity.value), quantity.unit)


# Legacy helper aliases.
int_unit = int_quantity
float_unit = float_quantity
long_unit = long_quantity
complex_unit = complex_quantity
