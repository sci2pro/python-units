# -*- coding: utf-8 -*-
"""Unit definition types and unit algebra."""

from __future__ import annotations, division

from typing import Dict

from .dimension import Dimension
from .errors import InvalidUnitError, InvalidValueError, UnitCompatibilityError

_CANONICAL_UNITS: dict[Dimension, BaseUnit] = {}


def register_canonical_unit(unit: BaseUnit) -> None:
    """Register a preferred unit for a canonical dimension."""
    _CANONICAL_UNITS[unit.dimension] = unit


def resolve_unit(dimension: Dimension) -> BaseUnit:
    """Resolve a dimension to a preferred named unit when available."""
    unit = _CANONICAL_UNITS.get(dimension)
    if unit is not None:
        return clone_unit(unit)
    return BaseUnit(dimension=dimension)


def require_unit_instance(unit: object) -> None:
    """Validate that an object is a unit definition.

    Args:
        unit: Candidate unit definition object.

    Raises:
        InvalidUnitError: If ``unit`` is not a ``BaseUnit`` instance.
    """
    if not isinstance(unit, BaseUnit):
        raise InvalidUnitError('unit must be an instance of BaseUnit, got {}'.format(type(unit).__name__))


class BaseUnit(object):
    """Base class for unit definitions."""

    def __init__(self, dimension: Dimension | None = None) -> None:
        self._dimension = dimension or Dimension()

    @property
    def unit_dict(self) -> Dict[str, int]:
        """Return the base-unit exponent map for this unit definition."""
        return self.dimension.to_mapping()

    @unit_dict.setter
    def unit_dict(self, unit_dict: Dict[str, int]) -> None:
        self._dimension = Dimension.from_mapping(unit_dict)

    @property
    def dimension(self) -> Dimension:
        """Return the canonical dimension tuple for this unit."""
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Dimension) -> None:
        self._dimension = dimension

    def __eq__(self, unit2: object) -> bool:
        return isinstance(unit2, BaseUnit) and self.dimension == unit2.dimension

    def _combine(self, unit2: BaseUnit, operator_name: str) -> BaseUnit:
        require_unit_instance(unit2)
        if operator_name == 'mul':
            dimension = self.dimension * unit2.dimension
        else:
            dimension = self.dimension / unit2.dimension
        return resolve_unit(dimension)

    def __mul__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'mul')

    def __div__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'div')

    def __truediv__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'div')

    def __str__(self) -> str:
        return self.dimension.render()


class SIUnit(BaseUnit):
    """Template class for SI units."""

    @classmethod
    def define(cls, key: str, value: int = 1) -> SIUnit:
        """Define an SI unit or exponentiated SI dimension.

        Args:
            key: Symbol of the SI base dimension.
            value: Exponent to assign to that base dimension.

        Returns:
            A new SI unit definition.

        Raises:
            InvalidUnitError: If ``key`` is not a supported SI dimension.
            InvalidValueError: If ``value`` is not an integer exponent.
        """
        if key not in Dimension.symbols:
            raise InvalidUnitError('unknown SI unit key: {}'.format(key))
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidValueError('unit exponent must be an integer, got {}'.format(type(value).__name__))
        obj = cls(dimension=Dimension.from_mapping({key: value}))
        return obj


class DerivedUnit(BaseUnit):
    """Named unit derived from SI dimensions."""

    def __init__(self, dimension: Dimension | None = None, *args: object, **kwargs: object) -> None:
        super(DerivedUnit, self).__init__(dimension=dimension, *args, **kwargs)
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
        return super(DerivedUnit, self).__str__()

    @classmethod
    def define(cls, name: str, unit: BaseUnit) -> DerivedUnit:
        """Define a named derived unit.

        Args:
            name: Display symbol for the derived unit.
            unit: Underlying SI-compatible unit expression.

        Returns:
            A new named derived unit definition.

        Raises:
            InvalidUnitError: If ``unit`` is not a valid unit definition.
        """
        require_unit_instance(unit)
        obj = cls(dimension=unit.dimension)
        obj.name = name
        return obj

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.full_units


def clone_unit(unit: BaseUnit | None) -> BaseUnit:
    """Clone a unit definition while preserving its type.

    Args:
        unit: Unit definition to clone, or ``None`` for a dimensionless unit.

    Returns:
        A cloned unit definition.

    Raises:
        InvalidUnitError: If ``unit`` is neither ``None`` nor a ``BaseUnit``.
    """
    if unit is None:
        return SIUnit()
    require_unit_instance(unit)

    cloned_unit = unit.__class__(dimension=unit.dimension)
    if isinstance(unit, DerivedUnit):
        cloned_unit.name = unit.name
    return cloned_unit
