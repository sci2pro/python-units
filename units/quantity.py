# -*- coding: utf-8 -*-
"""Quantity type and quantity operations."""

from __future__ import division

from numbers import Number, Real

from .errors import InvalidValueError, UnitCompatibilityError, UnitOperandError
from .unit import BaseUnit, SIUnit, clone_unit


def _is_number(value):
    return isinstance(value, Number) and not isinstance(value, bool)


def _is_real_number(value):
    return isinstance(value, Real) and not isinstance(value, bool)


def _validate_numeric_value(value):
    if not _is_number(value):
        raise InvalidValueError('value must be a numeric scalar, got {}'.format(type(value).__name__))


def _require_quantity_operand(operand, operation):
    if not isinstance(operand, Quantity):
        raise UnitOperandError(
            'unsupported operand for {}: {}'.format(operation, type(operand).__name__)
        )


class Quantity(object):
    """A numeric value coupled to a unit definition."""

    def __init__(self, value, unit=None):
        _validate_numeric_value(value)
        self._value = value
        self._unit = clone_unit(unit)

    @property
    def value(self):
        """Numeric value."""
        return self._value

    @value.setter
    def value(self, value):
        _validate_numeric_value(value)
        self._value = value

    @property
    def unit(self):
        """Unit definition."""
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = clone_unit(unit)

    @property
    def is_unitless(self):
        """Return True when the quantity is dimensionless."""
        return all(exponent == 0 for exponent in self.unit.unit_dict.values())

    def _dimensionless_unit(self):
        return SIUnit()

    def _require_compatible_quantity(self, quantity2, operation):
        _require_quantity_operand(quantity2, operation)
        if self.unit != quantity2.unit:
            raise UnitCompatibilityError('units mismatch: {} and {}'.format(self.unit, quantity2.unit))

    def _require_real_scalar(self, value, operation):
        if not _is_real_number(value):
            raise UnitOperandError(
                'unsupported scalar for {}: {}'.format(operation, type(value).__name__)
            )

    def _require_numeric_scalar(self, value, operation):
        if not _is_number(value):
            raise UnitOperandError(
                'unsupported scalar for {}: {}'.format(operation, type(value).__name__)
            )

    @property
    def full_units(self):
        """Render derived units in their SI decomposition."""
        if not isinstance(self.unit, SIUnit):
            return '{} {}'.format(self.value, self.unit.full_units).strip()
        return str(self)

    def __add__(self, quantity2):
        self._require_compatible_quantity(quantity2, 'addition')
        return self.__class__(self.value + quantity2.value, self.unit)

    def __radd__(self, quantity2):
        return self.__add__(quantity2)

    def __sub__(self, quantity2):
        self._require_compatible_quantity(quantity2, 'subtraction')
        return self.__class__(self.value - quantity2.value, self.unit)

    def __rsub__(self, quantity2):
        self._require_compatible_quantity(quantity2, 'subtraction')
        return self.__class__(quantity2.value - self.value, self.unit)

    def __mul__(self, quantity2):
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value * quantity2.value, self.unit * quantity2.unit)
        self._require_numeric_scalar(quantity2, 'multiplication')
        return self.__class__(self.value * quantity2, self.unit)

    def __rmul__(self, quantity2):
        return self.__mul__(quantity2)

    def __div__(self, quantity2):
        return self.__truediv__(quantity2)

    def __rdiv__(self, quantity2):
        return self.__rtruediv__(quantity2)

    def __truediv__(self, quantity2):
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value / quantity2.value, self.unit / quantity2.unit)
        self._require_numeric_scalar(quantity2, 'division')
        return self.__class__(self.value / quantity2, self.unit)

    def __rtruediv__(self, quantity2):
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value / self.value, quantity2.unit / self.unit)
        self._require_numeric_scalar(quantity2, 'division')
        return self.__class__(quantity2 / self.value, self._dimensionless_unit() / self.unit)

    def __floordiv__(self, quantity2):
        if isinstance(quantity2, Quantity):
            return self.__class__(self.value // quantity2.value, self.unit / quantity2.unit)
        self._require_real_scalar(quantity2, 'floor division')
        return self.__class__(self.value // quantity2, self.unit)

    def __rfloordiv__(self, quantity2):
        if isinstance(quantity2, Quantity):
            return self.__class__(quantity2.value // self.value, quantity2.unit / self.unit)
        self._require_real_scalar(quantity2, 'floor division')
        return self.__class__(quantity2 // self.value, self._dimensionless_unit() / self.unit)

    def __mod__(self, quantity2):
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, 'modulo')
            return self.__class__(self.value % quantity2.value, self.unit)
        self._require_real_scalar(quantity2, 'modulo')
        return self.__class__(self.value % quantity2, self.unit)

    def __rmod__(self, quantity2):
        if isinstance(quantity2, Quantity):
            self._require_compatible_quantity(quantity2, 'modulo')
            return self.__class__(quantity2.value % self.value, self.unit)
        self._require_real_scalar(quantity2, 'modulo')
        return self.__class__(quantity2 % self.value, self._dimensionless_unit() / self.unit)

    def __divmod__(self, quantity2):
        return self.__floordiv__(quantity2), self.__mod__(quantity2)

    def __rdivmod__(self, quantity2):
        return self.__rfloordiv__(quantity2), self.__rmod__(quantity2)

    def __neg__(self):
        return self.__class__(-self.value, self.unit)

    def __pos__(self):
        return self.__class__(+self.value, self.unit)

    def __abs__(self):
        return self.__class__(abs(self.value), self.unit)

    def __complex__(self):
        raise TypeError('invalid conversion from Quantity object to complex')

    def __int__(self):
        raise TypeError('invalid conversion from Quantity object to int')

    def __float__(self):
        raise TypeError('invalid conversion from Quantity object to float')

    def __long__(self):
        raise TypeError('invalid conversion from Quantity object to long')

    def __str__(self):
        return '{} {}'.format(self.value, self.unit).strip()


def int_quantity(quantity):
    """Convert a quantity value to int while preserving its unit."""
    _require_quantity_operand(quantity, 'int conversion')
    return Quantity(int(quantity.value), quantity.unit)


def float_quantity(quantity):
    """Convert a quantity value to float while preserving its unit."""
    _require_quantity_operand(quantity, 'float conversion')
    return Quantity(float(quantity.value), quantity.unit)


def long_quantity(quantity):
    """Convert a quantity value to long/int while preserving its unit."""
    _require_quantity_operand(quantity, 'long conversion')
    return Quantity(int(quantity.value), quantity.unit)


def complex_quantity(quantity):
    """Convert a quantity value to complex while preserving its unit."""
    _require_quantity_operand(quantity, 'complex conversion')
    return Quantity(complex(quantity.value), quantity.unit)


# Legacy helper aliases.
int_unit = int_quantity
float_unit = float_quantity
long_unit = long_quantity
complex_unit = complex_quantity
