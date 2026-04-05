# -*- coding: utf-8 -*-
"""Unit definition types and unit algebra."""

from __future__ import annotations, division

from typing import Dict

from .errors import InvalidUnitError, InvalidValueError, UnitCompatibilityError


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

    def __init__(self) -> None:
        self._unit_dict: Dict[str, int] = {
            'A': 0,
            'cd': 0,
            'K': 0,
            'kg': 0,
            'm': 0,
            'mol': 0,
            's': 0,
        }

    @property
    def unit_dict(self) -> Dict[str, int]:
        """Return the base-unit exponent map for this unit definition."""
        return self._unit_dict

    @unit_dict.setter
    def unit_dict(self, unit_dict: Dict[str, int]) -> None:
        self._unit_dict = dict(unit_dict)

    def __eq__(self, unit2: object) -> bool:
        return isinstance(unit2, BaseUnit) and self.unit_dict == unit2.unit_dict

    def _combine(self, unit2: BaseUnit, operator_name: str) -> BaseUnit:
        require_unit_instance(unit2)
        if set(self.unit_dict) != set(unit2.unit_dict):
            raise UnitCompatibilityError(
                'unit systems mismatch: {} and {}'.format(sorted(self.unit_dict), sorted(unit2.unit_dict))
            )

        result_unit = self.__class__()
        for unit_name in self.unit_dict:
            if operator_name == 'mul':
                result_value = self.unit_dict[unit_name] + unit2.unit_dict[unit_name]
            else:
                result_value = self.unit_dict[unit_name] - unit2.unit_dict[unit_name]
            result_unit.unit_dict[unit_name] = result_value
        return result_unit

    def __mul__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'mul')

    def __div__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'div')

    def __truediv__(self, unit2: BaseUnit) -> BaseUnit:
        return self._combine(unit2, 'div')

    def __str__(self) -> str:
        unit_string = list()
        for key, value in self.unit_dict.items():
            if value == 0:
                continue
            if value == 1:
                unit_string.insert(0, key)
            elif value < 0:
                unit_string.append(key + '^' + str(value))
            else:
                unit_string.insert(0, key + '^' + str(value))
        return '·'.join(unit_string)


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
        obj = cls()
        if key not in obj.unit_dict:
            raise InvalidUnitError('unknown SI unit key: {}'.format(key))
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidValueError('unit exponent must be an integer, got {}'.format(type(value).__name__))
        obj.unit_dict[key] = value
        return obj


class DerivedUnit(BaseUnit):
    """Named unit derived from SI dimensions."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super(DerivedUnit, self).__init__(*args, **kwargs)
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
        obj = cls()
        obj.name = name
        obj.unit_dict = dict(unit.unit_dict)
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

    cloned_unit = unit.__class__()
    cloned_unit.unit_dict = dict(unit.unit_dict)
    if isinstance(unit, DerivedUnit):
        cloned_unit.name = unit.name
    return cloned_unit
