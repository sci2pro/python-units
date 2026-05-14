# -*- coding: utf-8 -*-
"""Unit definition types and unit algebra."""

from __future__ import annotations

from numbers import Number, Real
from types import MappingProxyType
from typing import Dict, Mapping

from core.errors import (
    InvalidUnitError,
    InvalidValueError,
    UnitCompatibilityError,
    UnitOperandError,
)
from models.dimension import Dimension, DimensionSystem, SI_DIMENSION_SYSTEM

_CANONICAL_UNITS: Mapping[Dimension, "BaseUnit"] = MappingProxyType({})
_REGISTERED_CANONICAL_UNITS: tuple["BaseUnit", ...] = ()


def register_canonical_unit(unit: "BaseUnit") -> None:
    """Validate a preferred unit against the static canonical SI registry."""
    require_unit_instance(unit)
    if not any(registered_unit == unit for registered_unit in _REGISTERED_CANONICAL_UNITS):
        raise InvalidUnitError(
            "canonical units are statically defined and cannot be registered"
        )


def require_unit_instance(unit: object) -> None:
    """Validate that an object is a unit definition."""
    if not isinstance(unit, BaseUnit):
        raise InvalidUnitError(
            "unit must be an instance of BaseUnit, got {}".format(type(unit).__name__)
        )


def validate_conversion_factor(conversion_factor: object) -> float:
    """Validate a multiplicative conversion factor and return it as float."""
    if (
        not isinstance(conversion_factor, Real)
        or isinstance(conversion_factor, bool)
        or conversion_factor <= 0
    ):
        raise InvalidValueError(
            "conversion factor must be a positive real scalar, got {}".format(
                type(conversion_factor).__name__
            )
        )
    return float(conversion_factor)


def validate_conversion_support(supports_conversion: object) -> bool:
    """Validate a conversion support flag and return it."""
    if not isinstance(supports_conversion, bool):
        raise InvalidValueError(
            "conversion support flag must be bool, got {}".format(
                type(supports_conversion).__name__
            )
        )
    return supports_conversion


def validate_display_exponents(
    display_exponents: Mapping[str, int] | None,
) -> Mapping[str, int] | None:
    """Validate optional display-unit exponent metadata."""
    if display_exponents is None:
        return None
    validated_exponents: dict[str, int] = {}
    for symbol, exponent in display_exponents.items():
        if not isinstance(symbol, str):
            raise InvalidValueError(
                "display unit symbols must be strings, got {}".format(
                    type(symbol).__name__
                )
            )
        if not isinstance(exponent, int) or isinstance(exponent, bool):
            raise InvalidValueError(
                "display unit exponents must be integers, got {}".format(
                    type(exponent).__name__
                )
            )
        if exponent != 0:
            validated_exponents[symbol] = exponent
    return MappingProxyType(validated_exponents)


def validate_conversion_offset(conversion_offset: object) -> float:
    """Validate an affine conversion offset and return it as float."""
    if not isinstance(conversion_offset, Real) or isinstance(conversion_offset, bool):
        raise InvalidValueError(
            "conversion offset must be a real scalar, got {}".format(
                type(conversion_offset).__name__
            )
        )
    return float(conversion_offset)


def validate_affine_conversion_support(
    conversion_offset: float,
    supports_conversion: bool,
) -> None:
    """Raise when an affine unit is incorrectly marked multiplicative."""
    if conversion_offset != 0.0 and supports_conversion:
        raise InvalidValueError(
            "units with nonzero conversion offsets cannot support multiplicative arithmetic"
        )


def clone_unit(unit: "BaseUnit | None") -> "BaseUnit":
    """Clone a unit definition while preserving its type."""
    if unit is None:
        return SIUnit()
    require_unit_instance(unit)

    try:
        cloned_unit = unit.__class__(
            dimension=unit.dimension,
            conversion_factor=unit.conversion_factor,
            conversion_offset=unit.conversion_offset,
            display_exponents=unit.display_exponents,
            supports_multiplicative_conversion=unit.supports_multiplicative_conversion,
        )
    except TypeError:
        cloned_unit = unit.__class__(dimension=unit.dimension)
        cloned_unit._conversion_factor = unit.conversion_factor
        cloned_unit._conversion_offset = unit.conversion_offset
        cloned_unit._display_exponents = unit.display_exponents
        cloned_unit._supports_multiplicative_conversion = (
            unit.supports_multiplicative_conversion
        )
    if isinstance(unit, DerivedUnit):
        cloned_unit.name = unit.name
    return cloned_unit


def resolve_unit(dimension: Dimension) -> "BaseUnit":
    """Resolve a dimension to a preferred named unit when available."""
    unit = _CANONICAL_UNITS.get(dimension)
    if unit is not None:
        return clone_unit(unit)
    return BaseUnit(dimension=dimension)


def unit_display_exponents(unit: "BaseUnit") -> Mapping[str, int] | None:
    """Return display exponent metadata for a unit when available."""
    if isinstance(unit, DerivedUnit) and unit.name:
        return {unit.name: 1}
    if unit.display_exponents:
        return unit.display_exponents
    display_exponents = {
        symbol: exponent
        for symbol, exponent in zip(unit.dimension.system.symbols, unit.dimension.exponents)
        if exponent != 0
    }
    if not display_exponents:
        return None
    return MappingProxyType(display_exponents)


def combine_display_exponents(
    left: "BaseUnit",
    right: "BaseUnit",
    operator_name: str,
) -> Mapping[str, int] | None:
    """Compose display exponent metadata for a product or quotient."""
    left_exponents = unit_display_exponents(left)
    right_exponents = unit_display_exponents(right)
    if left_exponents is None and right_exponents is None:
        return None
    combined: dict[str, int] = {}
    for symbol, exponent in (left_exponents or {}).items():
        combined[symbol] = combined.get(symbol, 0) + exponent
    sign = 1 if operator_name == "mul" else -1
    for symbol, exponent in (right_exponents or {}).items():
        combined[symbol] = combined.get(symbol, 0) + sign * exponent
    return MappingProxyType(
        {
            symbol: exponent
            for symbol, exponent in combined.items()
            if exponent != 0
        }
    )


def power_display_exponents(
    unit: "BaseUnit",
    exponent: int,
) -> Mapping[str, int] | None:
    """Return display exponent metadata for an exponentiated unit."""
    display_exponents = unit_display_exponents(unit)
    if display_exponents is None:
        return None
    return MappingProxyType(
        {
            symbol: value * exponent
            for symbol, value in display_exponents.items()
            if value * exponent != 0
        }
    )


def render_display_exponents(display_exponents: Mapping[str, int] | None) -> str | None:
    """Render optional display exponent metadata."""
    if display_exponents is None:
        return None
    unit_string: list[str] = []
    for symbol, exponent in display_exponents.items():
        if exponent == 1:
            unit_string.append(symbol)
        else:
            unit_string.append("{}^{}".format(symbol, exponent))
    return "·".join(unit_string)


class BaseUnit:
    """Base class for unit definitions."""

    dimension_system = SI_DIMENSION_SYSTEM

    def __init__(
        self,
        dimension: Dimension | None = None,
        conversion_factor: float = 1.0,
        conversion_offset: float = 0.0,
        display_exponents: Mapping[str, int] | None = None,
        display_name: str | None = None,
        supports_multiplicative_conversion: bool = True,
    ) -> None:
        self._dimension = dimension or Dimension(
            system=self.dimension_system,
            exponents=(0,) * len(self.dimension_system.symbols),
        )
        self._conversion_factor = validate_conversion_factor(conversion_factor)
        self._conversion_offset = validate_conversion_offset(conversion_offset)
        self._display_exponents = validate_display_exponents(
            {display_name: 1} if display_name is not None else display_exponents
        )
        supports_conversion = validate_conversion_support(
            supports_multiplicative_conversion
        )
        validate_affine_conversion_support(
            self._conversion_offset,
            supports_conversion,
        )
        self._supports_multiplicative_conversion = supports_conversion

    @property
    def unit_dict(self) -> Dict[str, int]:
        """Return the base-unit exponent map for this unit definition."""
        return self.dimension.to_mapping()

    @unit_dict.setter
    def unit_dict(self, unit_dict: Dict[str, int]) -> None:
        self._dimension = Dimension.from_mapping(unit_dict, system=self.dimension_system)

    @property
    def dimension(self) -> Dimension:
        """Return the canonical dimension tuple for this unit."""
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Dimension) -> None:
        self._dimension = dimension

    @property
    def conversion_factor(self) -> float:
        """Return the multiplicative factor to this dimension's base unit."""
        return self._conversion_factor

    @property
    def conversion_offset(self) -> float:
        """Return the additive offset to this dimension's base unit."""
        return self._conversion_offset

    @property
    def display_exponents(self) -> Mapping[str, int] | None:
        """Return display exponents for anonymous composite units."""
        return self._display_exponents

    @property
    def display_name(self) -> str | None:
        """Return an explicit display name for single-symbol anonymous units."""
        if self._display_exponents is None or len(self._display_exponents) != 1:
            return None
        symbol, exponent = next(iter(self._display_exponents.items()))
        if exponent == 1:
            return symbol
        return None

    @property
    def supports_multiplicative_conversion(self) -> bool:
        """Return whether this unit can use scale-only conversion."""
        return self._supports_multiplicative_conversion

    def __eq__(self, unit2: object) -> bool:
        if not isinstance(unit2, BaseUnit):
            return False
        if self.dimension != unit2.dimension:
            return False
        if self.conversion_factor != unit2.conversion_factor:
            return False
        if self.conversion_offset != unit2.conversion_offset:
            return False
        if self.display_exponents != unit2.display_exponents:
            return False
        if isinstance(self, DerivedUnit) or isinstance(unit2, DerivedUnit):
            return (
                isinstance(self, DerivedUnit)
                and isinstance(unit2, DerivedUnit)
                and self.name == unit2.name
                and (
                    self.supports_multiplicative_conversion
                    == unit2.supports_multiplicative_conversion
                )
            )
        return True

    def _combine(self, unit2: "BaseUnit", operator_name: str) -> "BaseUnit":
        require_unit_instance(unit2)
        if self.dimension.system != unit2.dimension.system:
            raise UnitCompatibilityError(
                "unit systems mismatch: {} and {}".format(
                    self.dimension.system.name,
                    unit2.dimension.system.name,
                )
            )
        if operator_name == "mul":
            dimension = self.dimension * unit2.dimension
            conversion_factor = self.conversion_factor * unit2.conversion_factor
        else:
            dimension = self.dimension / unit2.dimension
            conversion_factor = self.conversion_factor / unit2.conversion_factor
        supports_conversion = (
            self.supports_multiplicative_conversion
            and unit2.supports_multiplicative_conversion
        )
        if not supports_conversion:
            raise UnitCompatibilityError(
                "units cannot be combined multiplicatively: {} and {}".format(
                    self,
                    unit2,
                )
            )
        display_exponents = combine_display_exponents(self, unit2, operator_name)
        if dimension.system != SI_DIMENSION_SYSTEM:
            return self.__class__(
                dimension=dimension,
                conversion_factor=conversion_factor,
                display_exponents=display_exponents,
                supports_multiplicative_conversion=supports_conversion,
            )
        if supports_conversion and conversion_factor == 1.0:
            return resolve_unit(dimension)
        return BaseUnit(
            dimension=dimension,
            conversion_factor=conversion_factor,
            display_exponents=display_exponents,
            supports_multiplicative_conversion=supports_conversion,
        )

    def _quantity_from_scalar(self, value: Number) -> object:
        from core.quantity import Quantity, normalize_scalar

        if (
            not isinstance(self, DerivedUnit)
            and self.conversion_factor != 1.0
            and self.conversion_offset == 0.0
            and self.supports_multiplicative_conversion
        ):
            try:
                unit = self.__class__(
                    dimension=self.dimension,
                    supports_multiplicative_conversion=(
                        self.supports_multiplicative_conversion
                    ),
                )
            except TypeError:
                unit = self.__class__(dimension=self.dimension)
                unit._supports_multiplicative_conversion = (
                    self.supports_multiplicative_conversion
                )
                unit._conversion_offset = self.conversion_offset
            result_value = value * self.conversion_factor
            if self.conversion_factor.is_integer():
                result_value = normalize_scalar(result_value)
            return Quantity(result_value, unit)
        return Quantity(value, self)

    def __mul__(self, unit2: object) -> object:
        if isinstance(unit2, BaseUnit):
            return self._combine(unit2, "mul")
        if isinstance(unit2, Number) and not isinstance(unit2, bool):
            return self._quantity_from_scalar(unit2)
        raise UnitOperandError(
            "unsupported operand for multiplication: {}".format(type(unit2).__name__)
        )

    def __rmul__(self, unit2: object) -> object:
        if isinstance(unit2, Number) and not isinstance(unit2, bool):
            return self._quantity_from_scalar(unit2)
        raise UnitOperandError(
            "unsupported operand for multiplication: {}".format(type(unit2).__name__)
        )

    def __truediv__(self, unit2: object) -> "BaseUnit":
        if isinstance(unit2, BaseUnit):
            return self._combine(unit2, "div")
        raise UnitOperandError(
            "unsupported operand for division: {}".format(type(unit2).__name__)
        )

    def __pow__(self, exponent: object) -> "BaseUnit":
        if not isinstance(exponent, int) or isinstance(exponent, bool):
            raise InvalidValueError(
                "unit exponent must be an integer, got {}".format(type(exponent).__name__)
            )
        dimension = Dimension(
            system=self.dimension.system,
            exponents=tuple(value * exponent for value in self.dimension.exponents),
        )
        conversion_factor = self.conversion_factor**exponent
        if not self.supports_multiplicative_conversion:
            raise UnitCompatibilityError(
                "unit cannot be raised to a power: {}".format(self)
            )
        if (
            isinstance(self, DerivedUnit)
            and self.name
            and exponent != 1
            and self.conversion_factor == 1.0
        ):
            derived = DerivedUnit(
                dimension=dimension,
                conversion_factor=1.0,
                supports_multiplicative_conversion=(
                    self.supports_multiplicative_conversion
                ),
            )
            derived.name = "{}^{}".format(self.name, exponent)
            return derived
        if dimension.system != SI_DIMENSION_SYSTEM:
            return self.__class__(
                dimension=dimension,
                conversion_factor=conversion_factor,
                display_exponents=power_display_exponents(self, exponent),
                supports_multiplicative_conversion=(
                    self.supports_multiplicative_conversion
                ),
            )
        if self.supports_multiplicative_conversion and conversion_factor == 1.0:
            return resolve_unit(dimension)
        return BaseUnit(
            dimension=dimension,
            conversion_factor=conversion_factor,
            display_exponents=power_display_exponents(self, exponent),
            supports_multiplicative_conversion=self.supports_multiplicative_conversion,
        )

    def __str__(self) -> str:
        display_name = render_display_exponents(self.display_exponents)
        if display_name is not None:
            return display_name
        return self.dimension.render()


class SIUnit(BaseUnit):
    """Template class for SI units."""

    @classmethod
    def define(
        cls,
        key: str,
        value: int = 1,
        conversion_factor: float = 1.0,
        conversion_offset: float = 0.0,
    ) -> "SIUnit":
        """Define an SI unit or exponentiated SI dimension."""
        if key not in cls.dimension_system.symbols:
            raise InvalidUnitError("unknown SI unit key: {}".format(key))
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidValueError(
                "unit exponent must be an integer, got {}".format(type(value).__name__)
            )
        return cls(
            dimension=Dimension.from_mapping({key: value}, system=cls.dimension_system),
            conversion_factor=conversion_factor,
            conversion_offset=conversion_offset,
        )


class CustomUnitBase(BaseUnit):
    """Base class for non-SI unit systems."""

    dimension_system = DimensionSystem("custom", ())

    @classmethod
    def define(
        cls,
        key: str,
        value: int = 1,
        conversion_factor: float = 1.0,
        conversion_offset: float = 0.0,
    ) -> "CustomUnitBase":
        """Define a custom base unit within the subclass dimension system."""
        if key not in cls.dimension_system.symbols:
            raise InvalidUnitError("unknown custom unit key: {}".format(key))
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidValueError(
                "unit exponent must be an integer, got {}".format(type(value).__name__)
            )
        return cls(
            dimension=Dimension.from_mapping({key: value}, system=cls.dimension_system),
            conversion_factor=conversion_factor,
            conversion_offset=conversion_offset,
        )


class DerivedUnit(BaseUnit):
    """Named unit derived from SI dimensions."""

    def __init__(self, dimension: Dimension | None = None, *args: object, **kwargs: object) -> None:
        super().__init__(dimension=dimension, *args, **kwargs)
        self._name: str | None = None

    @property
    def name(self) -> str | None:
        """Return the display name for the derived unit."""
        return self._name

    @name.setter
    def name(self, name: str | None) -> None:
        self._name = name

    @property
    def full_units(self) -> str:
        """Return the unit expressed in SI base dimensions."""
        return super().__str__()

    @classmethod
    def define(
        cls,
        name: str,
        unit: BaseUnit,
        conversion_factor: float | None = None,
        conversion_offset: float | None = None,
        supports_multiplicative_conversion: bool | None = None,
    ) -> "DerivedUnit":
        """Define a named derived unit."""
        require_unit_instance(unit)
        obj = cls(
            dimension=unit.dimension,
            conversion_factor=(
                unit.conversion_factor
                if conversion_factor is None
                else conversion_factor
            ),
            conversion_offset=(
                unit.conversion_offset
                if conversion_offset is None
                else conversion_offset
            ),
            supports_multiplicative_conversion=(
                unit.supports_multiplicative_conversion
                if supports_multiplicative_conversion is None
                else supports_multiplicative_conversion
            ),
        )
        obj.name = name
        return obj

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.full_units


def _build_canonical_units() -> tuple[Mapping[Dimension, BaseUnit], tuple[BaseUnit, ...]]:
    ampere = SIUnit.define("A")
    candela = SIUnit.define("cd")
    kelvin = SIUnit.define("K")
    kilogram = SIUnit.define("kg")
    metre = SIUnit.define("m")
    mole = SIUnit.define("mol")
    second = SIUnit.define("s")

    newton = DerivedUnit.define("N", kilogram * metre / second / second)
    pascal = DerivedUnit.define("Pa", newton / metre / metre)
    joule = DerivedUnit.define("J", newton * metre)
    watt = DerivedUnit.define("W", joule / second)
    coulomb = DerivedUnit.define("C", second * ampere)
    volt = DerivedUnit.define("V", watt / ampere)
    farad = DerivedUnit.define("F", coulomb / volt)
    ohm = DerivedUnit.define("Ω", volt / ampere)
    siemens = DerivedUnit.define("S", ampere / volt)
    weber = DerivedUnit.define("Wb", volt * second)
    tesla = DerivedUnit.define("T", weber / metre / metre)
    henry = DerivedUnit.define("H", weber / ampere)
    steradian = DerivedUnit.define("sr", metre * metre / metre / metre)
    lumen = DerivedUnit.define("lm", candela * steradian)
    lux = DerivedUnit.define("lx", lumen / metre / metre)

    registered_units = (
        ampere,
        candela,
        kelvin,
        kilogram,
        metre,
        mole,
        second,
        newton,
        pascal,
        joule,
        watt,
        coulomb,
        volt,
        farad,
        ohm,
        siemens,
        weber,
        tesla,
        henry,
        lumen,
        lux,
    )
    preferred_units = (
        ampere,
        kelvin,
        kilogram,
        metre,
        mole,
        second,
        newton,
        pascal,
        joule,
        watt,
        coulomb,
        volt,
        farad,
        ohm,
        siemens,
        weber,
        tesla,
        henry,
        lumen,
        lux,
    )
    return MappingProxyType({unit.dimension: unit for unit in preferred_units}), registered_units


_CANONICAL_UNITS, _REGISTERED_CANONICAL_UNITS = _build_canonical_units()
