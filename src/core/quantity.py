# -*- coding: utf-8 -*-
"""Quantity type and quantity operations."""

from __future__ import annotations

from core.deprecations import deprecated_call
from core.errors import InvalidValueError, UnitCompatibilityError, UnitOperandError
from core.unit_definitions import (
    BaseUnit,
    DerivedUnit,
    SIUnit,
    clone_unit,
    require_unit_instance,
)
from models.dimension import SI_DIMENSION_SYSTEM
from utils.numbers import Scalar, is_number, is_real_number, validate_numeric_value


def require_quantity_operand(operand: object, operation: str) -> None:
    """Raise when an operand is not a quantity."""
    if not isinstance(operand, Quantity):
        raise UnitOperandError(
            "unsupported operand for {}: {}".format(operation, type(operand).__name__)
        )


def normalize_scalar(value: Scalar) -> Scalar:
    """Return ``int`` for exact integer floats, otherwise return ``value``."""
    if isinstance(value, float):
        nearest_integer = round(value)
        if abs(value - nearest_integer) < 1e-12:
            return int(nearest_integer)
    return value


def format_scalar(value: Scalar) -> str:
    """Render numeric values with minimal cleanup for binary-float noise."""
    if isinstance(value, float):
        if value.is_integer():
            return str(value)
        nearest_integer = round(value)
        if abs(value - nearest_integer) < 1e-12:
            return str(int(nearest_integer))
        rounded_value = round(value, 12)
        text = repr(value)
        if (
            abs(value - rounded_value) < 1e-12
            and ("000000" in text or "999999" in text)
        ):
            return str(rounded_value)
    return str(value)


def normalize_product(value: Scalar, left: Scalar, right: Scalar) -> Scalar:
    """Normalize exact integer products only when both inputs were integers."""
    if isinstance(left, int) and isinstance(right, int):
        return normalize_scalar(value)
    return value


def normalize_reverse_floor(value: Scalar, denominator: "Quantity") -> Scalar:
    """Preserve legacy int display for unscaled integer reverse floor division."""
    if (
        denominator.unit.conversion_factor == 1.0
        and isinstance(denominator.value, int)
    ):
        return normalize_scalar(value)
    return value


def normalize_result_unit(result_unit: BaseUnit) -> BaseUnit:
    """Return a renderable result unit with no hidden anonymous scale."""
    if isinstance(result_unit, DerivedUnit) or result_unit.conversion_factor == 1.0:
        return result_unit
    try:
        return result_unit.__class__(
            dimension=result_unit.dimension,
            conversion_offset=result_unit.conversion_offset,
            supports_multiplicative_conversion=(
                result_unit.supports_multiplicative_conversion
            ),
        )
    except TypeError:
        unit = result_unit.__class__(dimension=result_unit.dimension)
        unit._conversion_offset = result_unit.conversion_offset
        unit._supports_multiplicative_conversion = (
            result_unit.supports_multiplicative_conversion
        )
        return unit


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

    def _base_value(self) -> Scalar:
        self._require_multiplicative_unit("multiplicative arithmetic")
        return self.value * self.unit.conversion_factor

    def _require_multiplicative_unit(self, operation: str) -> None:
        if not self.unit.supports_multiplicative_conversion:
            raise UnitCompatibilityError(
                "unit cannot be used in {}: {}".format(operation, self.unit)
            )

    def _canonical_value(self) -> Scalar:
        return self.value * self.unit.conversion_factor + self.unit.conversion_offset

    def to(self, target_unit: BaseUnit) -> "Quantity":
        """
        Convert this quantity to a compatible target unit.

        Args:
            target_unit: Unit definition with the same dimension.

        Returns:
            Quantity expressed in ``target_unit``.

        Raises:
            InvalidUnitError: If ``target_unit`` is not a unit definition.
            UnitCompatibilityError: If dimensions differ.
        """
        require_unit_instance(target_unit)
        if self.unit.dimension != target_unit.dimension:
            raise UnitCompatibilityError(
                "cannot convert {} to {}".format(self.unit, target_unit)
            )
        return self.__class__(
            normalize_scalar(
                (self._canonical_value() - target_unit.conversion_offset)
                / target_unit.conversion_factor
            ),
            target_unit,
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
            result_unit = self.unit * quantity2.unit
            result_value = self._base_value() * quantity2._base_value()
            return self.__class__(
                normalize_product(result_value, self.value, quantity2.value),
                normalize_result_unit(result_unit),
            )
        if isinstance(quantity2, BaseUnit):
            result_unit = self.unit * quantity2
            result_value = (
                self._base_value()
                * quantity2.conversion_factor
            )
            return self.__class__(
                normalize_scalar(result_value),
                normalize_result_unit(result_unit),
            )
        self._require_numeric_scalar(quantity2, "multiplication")
        self._require_multiplicative_unit("multiplication")
        return self.__class__(self.value * quantity2, self.unit)

    def __rmul__(self, quantity2: object) -> "Quantity":
        return self.__mul__(quantity2)

    def __truediv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            result_unit = self.unit / quantity2.unit
            result_value = self._base_value() / quantity2._base_value()
            return self.__class__(result_value, normalize_result_unit(result_unit))
        if isinstance(quantity2, BaseUnit):
            result_unit = self.unit / quantity2
            result_value = (
                self._base_value()
                / quantity2.conversion_factor
            )
            return self.__class__(
                normalize_scalar(result_value),
                normalize_result_unit(result_unit),
            )
        self._require_numeric_scalar(quantity2, "division")
        self._require_multiplicative_unit("division")
        return self.__class__(self.value / quantity2, self.unit)

    def __rtruediv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            result_unit = quantity2.unit / self.unit
            result_value = quantity2._base_value() / self._base_value()
            return self.__class__(result_value, normalize_result_unit(result_unit))
        self._require_numeric_scalar(quantity2, "division")
        result_unit = self._dimensionless_unit() / self.unit
        result_value = quantity2 / self._base_value()
        return self.__class__(result_value, normalize_result_unit(result_unit))

    def __floordiv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            result_unit = self.unit / quantity2.unit
            result_value = self._base_value() // quantity2._base_value()
            return self.__class__(result_value, normalize_result_unit(result_unit))
        self._require_real_scalar(quantity2, "floor division")
        self._require_multiplicative_unit("floor division")
        return self.__class__(self.value // quantity2, self.unit)

    def __rfloordiv__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            result_unit = quantity2.unit / self.unit
            result_value = quantity2._base_value() // self._base_value()
            return self.__class__(
                normalize_scalar(result_value),
                normalize_result_unit(result_unit),
            )
        self._require_real_scalar(quantity2, "floor division")
        result_unit = self._dimensionless_unit() / self.unit
        result_value = quantity2 // self._base_value()
        return self.__class__(
            normalize_reverse_floor(result_value, self),
            normalize_result_unit(result_unit),
        )

    def __mod__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, "modulo")
            return self.__class__(self.value % quantity2.value, self.unit)
        self._require_real_scalar(quantity2, "modulo")
        self._require_multiplicative_unit("modulo")
        return self.__class__(self.value % quantity2, self.unit)

    def __rmod__(self, quantity2: object) -> "Quantity":
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, "modulo")
            return self.__class__(quantity2.value % self.value, self.unit)
        self._require_real_scalar(quantity2, "modulo")
        result_unit = self._dimensionless_unit() / self.unit
        result_value = quantity2 % self._base_value()
        return self.__class__(
            normalize_scalar(result_value),
            normalize_result_unit(result_unit),
        )

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
        result_unit = self.unit ** exponent
        result_value = self._base_value() ** exponent
        return self.__class__(
            normalize_scalar(result_value),
            normalize_result_unit(result_unit),
        )

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
        return "{} {}".format(format_scalar(self.value), self.unit).strip()


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
    return deprecated_call(
        "long_quantity",
        "int_quantity",
        "1.0.0",
        lambda: int_quantity(quantity),
    )


def complex_quantity(quantity: Quantity) -> Quantity:
    """Convert a quantity value to complex while preserving its unit."""
    require_quantity_operand(quantity, "complex conversion")
    return Quantity(complex(quantity.value), quantity.unit)


def convert(quantity: Quantity, target_unit: BaseUnit) -> Quantity:
    """
    Convert a quantity to a compatible target unit.

    Args:
        quantity: Quantity to convert.
        target_unit: Unit definition with the same dimension.

    Returns:
        Quantity expressed in ``target_unit``.

    Raises:
        UnitOperandError: If ``quantity`` is not a Quantity.
        InvalidUnitError: If ``target_unit`` is not a unit definition.
        UnitCompatibilityError: If dimensions differ.
    """
    require_quantity_operand(quantity, "conversion")
    return quantity.to(target_unit)


def value(quantity: Quantity) -> Scalar:
    """
    Return the numeric value of a quantity without converting it.

    Args:
        quantity: Quantity to inspect.

    Returns:
        Numeric value stored on the quantity.

    Raises:
        UnitOperandError: If ``quantity`` is not a Quantity.
    """
    require_quantity_operand(quantity, "value extraction")
    return quantity.value


def unit(quantity: Quantity) -> BaseUnit:
    """
    Return the unit definition of a quantity.

    Args:
        quantity: Quantity to inspect.

    Returns:
        Unit definition stored on the quantity.

    Raises:
        UnitOperandError: If ``quantity`` is not a Quantity.
    """
    require_quantity_operand(quantity, "unit extraction")
    return quantity.unit


def multiplier(quantity_or_unit: Quantity | BaseUnit) -> float:
    """
    Return the multiplicative factor to the canonical base dimension.

    Args:
        quantity_or_unit: Quantity or unit definition to inspect.

    Returns:
        Multiplicative factor for the unit carried by the input.

    Raises:
        UnitOperandError: If the input is neither Quantity nor BaseUnit.
    """
    if isinstance(quantity_or_unit, Quantity):
        return quantity_or_unit.unit.conversion_factor
    if isinstance(quantity_or_unit, BaseUnit):
        return quantity_or_unit.conversion_factor
    raise UnitOperandError(
        "unsupported operand for multiplier extraction: {}".format(
            type(quantity_or_unit).__name__
        )
    )


def int_unit(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``int_quantity``."""
    return deprecated_call(
        "int_unit",
        "int_quantity",
        "1.0.0",
        lambda: int_quantity(quantity),
    )


def float_unit(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``float_quantity``."""
    return deprecated_call(
        "float_unit",
        "float_quantity",
        "1.0.0",
        lambda: float_quantity(quantity),
    )


def long_unit(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``int_quantity``."""
    return deprecated_call(
        "long_unit",
        "int_quantity",
        "1.0.0",
        lambda: int_quantity(quantity),
    )


def complex_unit(quantity: Quantity) -> Quantity:
    """Legacy compatibility helper equivalent to ``complex_quantity``."""
    return deprecated_call(
        "complex_unit",
        "complex_quantity",
        "1.0.0",
        lambda: complex_quantity(quantity),
    )
