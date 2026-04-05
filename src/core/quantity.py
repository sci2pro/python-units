# -*- coding: utf-8 -*-
"""Quantity type and quantity operations."""

from __future__ import annotations

from core.errors import InvalidValueError, UnitCompatibilityError, UnitOperandError
from core.unit_definitions import BaseUnit, SIUnit, clone_unit
from models.dimension import SI_DIMENSION_SYSTEM
from utils.numbers import Scalar, is_number, is_real_number, validate_numeric_value


def require_quantity_operand(operand: object, operation: str) -> None:
    """Raise when an operand is not a quantity."""
    if not isinstance(operand, Quantity):
        raise UnitOperandError(
            "unsupported operand for {}: {}".format(operation, type(operand).__name__)
        )


class Quantity:
    """A numeric value coupled to a unit definition."""

    def __init__(self, value: Scalar, unit: BaseUnit | None = None) -> None:
        validate_numeric_value(value)
        self._value = value
        self._unit = clone_unit(unit)

    @property
    def value(self) -> Scalar:
        """Return the numeric value for the quantity."""
        return self._value

    @value.setter
    def value(self, value: Scalar) -> None:
        validate_numeric_value(value)
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

    @property
    def full_units(self) -> str:
        """Render derived units in their SI decomposition."""
        if self.unit.dimension.system != SI_DIMENSION_SYSTEM:
            return str(self)
        if not self.is_unitless and not isinstance(self.unit, SIUnit):
            return "{} {}".format(self.value, self.unit.full_units).strip()
        return str(self)

    def _dimensionless_unit(self) -> SIUnit:
        return SIUnit()

    def _require_compatible_quantity(self, quantity2: object, operation: str) -> None:
        require_quantity_operand(quantity2, operation)
        if self.unit != quantity2.unit:
            raise UnitCompatibilityError(
                "units mismatch: {} and {}".format(self.unit, quantity2.unit)
            )

    def _require_real_scalar(self, value: object, operation: str) -> None:
        if not is_real_number(value):
            raise UnitOperandError(
                "unsupported scalar for {}: {}".format(operation, type(value).__name__)
            )

    def _require_numeric_scalar(self, value: object, operation: str) -> None:
        if not is_number(value):
            raise UnitOperandError(
                "unsupported scalar for {}: {}".format(operation, type(value).__name__)
            )

    def __add__(self, quantity2: object) -> "Quantity":
        self._require_compatible_quantity(quantity2, "addition")
        return self.__class__(self.value + quantity2.value, self.unit)

    def __radd__(self, quantity2: object) -> "Quantity":
        return self.__add__(quantity2)

    def __sub__(self, quantity2: object) -> "Quantity":
        self._require_compatible_quantity(quantity2, "subtraction")
        return self.__class__(self.value - quantity2.value, self.unit)

    def __rsub__(self, quantity2: object) -> "Quantity":
        self._require_compatible_quantity(quantity2, "subtraction")
        return self.__class__(quantity2.value - self.value, self.unit)

    def __mul__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value * quantity2.value, self.unit * quantity2.unit)
        if isinstance(quantity2, BaseUnit):
            return self.__class__(self.value, self.unit * quantity2)
        self._require_numeric_scalar(quantity2, "multiplication")
        return self.__class__(self.value * quantity2, self.unit)

    def __rmul__(self, quantity2: object) -> "Quantity":
        return self.__mul__(quantity2)

    def __truediv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value / quantity2.value, self.unit / quantity2.unit)
        if isinstance(quantity2, BaseUnit):
            return self.__class__(self.value, self.unit / quantity2)
        self._require_numeric_scalar(quantity2, "division")
        return self.__class__(self.value / quantity2, self.unit)

    def __rtruediv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value / self.value, quantity2.unit / self.unit)
        self._require_numeric_scalar(quantity2, "division")
        return self.__class__(quantity2 / self.value, self._dimensionless_unit() / self.unit)

    def __floordiv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value // quantity2.value, self.unit / quantity2.unit)
        self._require_real_scalar(quantity2, "floor division")
        return self.__class__(self.value // quantity2, self.unit)

    def __rfloordiv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value // self.value, quantity2.unit / self.unit)
        self._require_real_scalar(quantity2, "floor division")
        return self.__class__(quantity2 // self.value, self._dimensionless_unit() / self.unit)

    def __mod__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, "modulo")
            return self.__class__(self.value % quantity2.value, self.unit)
        self._require_real_scalar(quantity2, "modulo")
        return self.__class__(self.value % quantity2, self.unit)

    def __rmod__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, "modulo")
            return self.__class__(quantity2.value % self.value, self.unit)
        self._require_real_scalar(quantity2, "modulo")
        return self.__class__(quantity2 % self.value, self._dimensionless_unit() / self.unit)

    def __divmod__(self, quantity2: object) -> tuple["Quantity", "Quantity"]:
        return self.__floordiv__(quantity2), self.__mod__(quantity2)

    def __rdivmod__(self, quantity2: object) -> tuple["Quantity", "Quantity"]:
        return self.__rfloordiv__(quantity2), self.__rmod__(quantity2)

    def __pow__(self, exponent: object) -> "Quantity":
        self._require_numeric_scalar(exponent, "power")
        if isinstance(exponent, complex):
            raise UnitOperandError("unsupported scalar for power: complex")
        if not self.is_unitless and (not isinstance(exponent, int) or isinstance(exponent, bool)):
            raise UnitOperandError(
                "unsupported scalar for power: {}".format(type(exponent).__name__)
            )
        if self.is_unitless:
            return self.__class__(self.value ** exponent, self.unit)
        return self.__class__(self.value ** exponent, self.unit ** exponent)

    def __neg__(self) -> "Quantity":
        return self.__class__(-self.value, self.unit)

    def __pos__(self) -> "Quantity":
        return self.__class__(+self.value, self.unit)

    def __abs__(self) -> "Quantity":
        return self.__class__(abs(self.value), self.unit)

    def __complex__(self) -> complex:
        raise TypeError("invalid conversion from Quantity object to complex")

    def __int__(self) -> int:
        raise TypeError("invalid conversion from Quantity object to int")

    def __float__(self) -> float:
        raise TypeError("invalid conversion from Quantity object to float")

    def __str__(self) -> str:
        return "{} {}".format(self.value, self.unit).strip()


def int_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to int while preserving its unit."""
    require_quantity_operand(quantity, "int conversion")
    return Quantity(int(quantity.value), quantity.unit)


def float_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to float while preserving its unit."""
    require_quantity_operand(quantity, "float conversion")
    return Quantity(float(quantity.value), quantity.unit)


def long_quantity(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``int_quantity``."""
    require_quantity_operand(quantity, "long conversion")
    return Quantity(int(quantity.value), quantity.unit)


def complex_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to complex while preserving its unit."""
    require_quantity_operand(quantity, "complex conversion")
    return Quantity(complex(quantity.value), quantity.unit)


int_unit = int_quantity
float_unit = float_quantity
long_unit = long_quantity
complex_unit = complex_quantity
