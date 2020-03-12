# -*- coding: utf-8 -*-
# units
"""
===============================================================================
Units
===============================================================================
A Python library to represent numbers with units.
Copyright (C) 2017  Paul K. Korir
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
:TODO: add multipliers
"""
from __future__ import division, print_function

import sys

__author__ = "Paul K. Korir"
__email__ = "paul.korir@gmail.com"
__date__ = "2017-06-01"

"""
:TODO: methods to add
object.__pow__(self, other[, modulo])
object.__lshift__(self, other)
object.__rshift__(self, other)
object.__and__(self, other)
object.__xor__(self, other)
object.__or__(self, other)

object.__rpow__(self, other)
object.__rlshift__(self, other)
object.__rrshift__(self, other)
object.__rand__(self, other)
object.__rxor__(self, other)
object.__ror__(self, other)

object.__iadd__(self, other)
object.__isub__(self, other)
object.__imul__(self, other)
object.__idiv__(self, other)
object.__itruediv__(self, other)
object.__ifloordiv__(self, other)
object.__imod__(self, other)
object.__ipow__(self, other[, modulo])
object.__ilshift__(self, other)
object.__irshift__(self, other)
object.__iand__(self, other)
object.__ixor__(self, other)
object.__ior__(self, other)

object.__invert__(self)

        object.__oct__(self)
object.__hex__(self)

currency and special cases e.g. £ 32 per person instead of 32 £·person^-1 !!!
"""


class UnitsError(Exception):
    """Units Error exception
    
    Raised when an operation improperly uses units
    """

    def __init__(self, *args, **kwargs):
        super(UnitsError, self).__init__(*args, **kwargs)


class BaseUnit(object):
    """Base class"""

    def __init__(self):
        self.__unit_dict = {
            'A': 0,
            'cd': 0,
            'K': 0,
            'kg': 0,
            'm': 0,
            'mol': 0,
            's': 0,
        }

    @property
    def unit_dict(self):
        """A dictionary to hold base units
        
        The base units are the Systeme International (SI) units 
        """
        return self.__unit_dict

    @unit_dict.setter
    def unit_dict(self, unit_dict):
        self.__unit_dict = unit_dict

    def __eq__(self, unit2):
        if self.unit_dict == unit2.unit_dict:
            return True
        else:
            return False

    def __mul__(self, unit2):
        result_unit = self.__class__()
        for unit_name in self.unit_dict:
            result_unit.unit_dict[unit_name] = self.unit_dict[unit_name] + unit2.unit_dict[unit_name]
        return result_unit

    def __div__(self, unit2):
        result_unit = self.__class__()
        for unit_name in self.unit_dict:
            result_unit.unit_dict[unit_name] = self.unit_dict[unit_name] - unit2.unit_dict[unit_name]
        return result_unit

    def __truediv__(self, unit2):
        result_unit = self.__class__()
        for unit_name in self.unit_dict:
            result_unit.unit_dict[unit_name] = self.unit_dict[unit_name] - unit2.unit_dict[unit_name]
        return result_unit

    def __str__(self):
        unit_string = list()
        # string = ''
        for k, v in self.unit_dict.items():
            if v == 0:
                continue
            elif v == 1:
                unit_string.insert(0, k)
            elif v < 0:
                unit_string.append(k + '^' + str(v))
            else:
                unit_string.insert(0, k + '^' + str(v))
        return '·'.join(unit_string)


class SIUnit(BaseUnit):
    """Template class for SI units"""

    def __init__(self, *args, **kwargs):
        super(SIUnit, self).__init__(*args, **kwargs)

    @classmethod
    def define(cls, key, value=1):
        """Constructor to define an SI unit
        
        Example:
        
        ::
        
            ampere = SIUnit.define('A')
        """
        obj = cls()
        assert key in obj.unit_dict.keys()
        assert isinstance(value, int)
        obj.unit_dict[key] = value
        return obj


class DerivedUnit(BaseUnit):
    """Class for units derived from SI units"""

    def __init__(self, *args, **kwargs):
        super(DerivedUnit, self).__init__(*args, **kwargs)
        self.__name = None

    @property
    def name(self):
        """Unit name"""
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def full_units(self):
        """The unit in terms of SI units"""
        return super(DerivedUnit, self).__str__()

    @classmethod
    def define(cls, name, unit):
        """Constructor to define an SI unit
        
        Example:
        
        ::
            
            hertz = DerivedUnit.define('Hz', SIUnit() / second)
        
        defines the unit for measuring frequency (hertz, Hz). SIUnit()
        with not arguments is unitless.
        """
        obj = cls()
        obj.name = name
        obj.unit_dict = unit.unit_dict
        return obj

    def __str__(self):
        return self.name


class UnitOperandError(Exception):
    """Error due to wrong application of operands"""

    def __init__(self, *args, **kwargs):
        super(UnitOperandError, self).__init__(*args, **kwargs)


# SI units
ampere = SIUnit.define('A')
candela = SIUnit.define('cd')
kelvin = SIUnit.define('K')
kilogram = SIUnit.define('kg')
metre = SIUnit.define('m')
mole = SIUnit.define('mol')
second = SIUnit.define('s')

# derived units
radian = DerivedUnit.define('rad', metre / metre)
steradian = DerivedUnit.define('sr', metre * metre / metre / metre)
hertz = DerivedUnit.define('Hz', SIUnit() / second)
newton = DerivedUnit.define('N', kilogram * metre / second / second)
pascal = DerivedUnit.define('Pa', newton / metre / metre)
joule = DerivedUnit.define('J', newton * metre)
watt = DerivedUnit.define('W', joule / second)
coulomb = DerivedUnit.define('C', second * ampere)
volt = DerivedUnit.define('V', watt / ampere)
farad = DerivedUnit.define('F', coulomb / volt)
ohm = DerivedUnit.define('Ω', volt / ampere)
siemens = DerivedUnit.define('S', ampere / volt)
weber = DerivedUnit.define('Wb', volt * second)
tesla = DerivedUnit.define('T', weber / metre / metre)
henry = DerivedUnit.define('H', weber / ampere)
degree_celcius = DerivedUnit.define('°C', kelvin)
lumen = DerivedUnit.define('lm', candela * steradian)
lux = DerivedUnit.define('lx', lumen / metre / metre)
becquerel = DerivedUnit.define('Bq', SIUnit() / second)
gray = DerivedUnit.define('Gy', joule / kilogram)
sievert = DerivedUnit.define('Sv', joule / kilogram)
katal = DerivedUnit.define('kat', mole / second)


class Unit(object):
    """Class to create unit-aware numbers"""

    def __init__(self, value, unit=None):
        assert isinstance(unit, BaseUnit) or unit is None
        assert isinstance(value, int) or isinstance(value, float) or isinstance(value, complex) or isinstance(value,
                                                                                                              long)  # long, double? etc.
        self.__value = value
        self.__unit = unit

    @property
    def value(self):
        """Numeric value"""
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def unit(self):
        """Unit"""
        return self.__unit

    @unit.setter
    def unit(self, unit):
        if isinstance(unit, unit):
            self.__unit = unit
        else:
            raise UnitsError('units mismatch: {} and {}'.format(self.unit, type(unit)))

    @property
    def full_units(self):
        """Derived units in terms of SI units
        
        Applies to derived units.
        
        ::
        
            # pascal
            print(Unit(758, pascal))
            print(Unit(758, pascal).full_units)
        
        will print()
        
        ::
        
            758 Pa
            758 kg·m^-1·s^-2
        """
        if not isinstance(self.__unit, SIUnit):
            return '{} {}'.format(self.value, self.__unit.full_units)
        else:
            return '{} {}'.format(self.value, self.__unit)

    def __add__(self, unit2):
        if isinstance(unit2, Unit):
            if self.unit == unit2.unit:
                return Unit(self.value + unit2.value, self.unit)
            else:
                raise UnitsError('units mismatch: {} and {}'.format(self.unit, unit2.unit))
        else:
            raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __radd__(self, unit2):
        return self.__add__(unit2)

    def __sub__(self, unit2):
        if isinstance(unit2, Unit):
            if self.unit == unit2.unit:
                return Unit(self.value - unit2.value, self.unit)
            else:
                raise UnitsError('units mismatch: {} and {}'.format(self.unit, unit2.unit))
        else:
            raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __rsub__(self, unit2):
        return self.__sub__(unit2)

    def __mul__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value * unit2.value, self.unit * unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value * unit2, self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __rmul__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value * unit2.value, self.unit * unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value * unit2, self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __div__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value / unit2.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value / unit2, self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __rdiv__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(unit2.value / self.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(unit2 / self.value, SIUnit() / self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __truediv__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value / unit2.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value / unit2, self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __rtruediv__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(unit2.value / self.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(unit2 / self.value, SIUnit() / self.unit)
        # else:
        #     raise UnitOperandError('not object of type unit: {}'.format(type(unit2)))

    def __floordiv__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value // unit2.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value // unit2, self.unit)

    def __rfloordiv__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(unit2.value // self.value, unit2.unit / self.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(unit2 // self.value, SIUnit() / self.unit)

    def __mod__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(self.value % unit2.value, self.unit / unit2.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(self.value % unit2, self.unit)

    def __rmod__(self, unit2):
        if isinstance(unit2, Unit):
            return Unit(unit2.value % self.value, unit2.unit / self.unit)
        elif isinstance(unit2, int) or isinstance(unit2, float) or isinstance(unit2, long) or isinstance(unit2,
                                                                                                         complex) or isinstance(
            unit2, oct) or isinstance(unit2, hex):
            return Unit(unit2 % self.value, SIUnit() / self.unit)

    def __divmod__(self, unit2):
        return self.__floordiv__(unit2), self.__mod__(unit2)

    def __rdivmod__(self, unit2):
        return self.__rfloordiv__(unit2), self.__rmod__(unit2)

    def __neg__(self):
        return Unit(-self.value, self.unit)

    def __pos__(self):
        return Unit(+self.value, self.unit)

    def __abs__(self):
        return Unit(abs(self.value), self.unit)

    def __complex__(self):
        raise TypeError('invalid conversion from Unit object to complex')

    def __int__(self):
        raise TypeError('invalid conversion from Unit object to int')

    def __float__(self):
        raise TypeError('invalid conversion from Unit object to float')

    def __long__(self):
        raise TypeError('invalid conversion from Unit object to long')

    def __str__(self):
        return '{} {}'.format(self.value, self.__unit).strip(' ')
    # def __repr__(self):
    #     return '{} {}'.format(self.value, self.__unit)


def int_unit(unit):
    """Convert a Unit object to have an integer

    :param unit: a Unit object
    :type unit: Unit
    :return unit: a Unit object with integer value
    :rtype unit: Unit
    """
    return Unit(int(unit.value), unit.unit)


def float_unit(unit):
    """Convert a Unit object to have an float

    :param unit: a Unit object
    :type unit: Unit
    :return unit: a Unit object with integer value
    :rtype unit: Unit
    """
    return Unit(float(unit.value), unit.unit)


def long_unit(unit):
    """Convert a Unit object to have a long

    :param unit: a Unit object
    :type unit: Unit
    :return unit: a Unit object with integer value
    :rtype unit: Unit
    """
    return Unit(int(unit.value), unit.unit)


def complex_unit(unit):
    """Convert a Unit object to have an integer

    :param unit: a Unit object
    :type unit: Unit
    :return unit: a Unit object with integer value
    :rtype unit: Unit
    """
    return Unit(complex(unit.value), unit.unit)


def main():
    x = Unit(1, metre)
    y = Unit(2, metre)
    print(x)
    print(x + y)
    print(x * y)
    print(x / y)
    z = Unit(3, second)
    print(x / z)
    i = Unit(5.7, ampere)
    print(z * i)
    print(Unit(272.93, kilogram * metre / second / second))
    print(Unit(20.232, kilogram * metre * metre / second / second / ampere))
    print(Unit(272.93, kilogram * metre / second / second) * Unit(20.232,
                                                                  kilogram * metre * metre / second / second / ampere))
    k = Unit(392.22, hertz)
    print(k)
    print(k.full_units)
    j = Unit(29302.33, SIUnit() / second)
    print(j)
    F = Unit(93.39, newton)
    print(F)
    print(F.full_units)
    P = Unit(758, pascal)
    print(P)
    print(P.full_units)
    print(Unit(93, becquerel).full_units)
    print(Unit(20, katal).full_units)
    print(2 * Unit(30, metre))
    print(2 / Unit(20, metre))
    print(Unit(20, metre) / 2)
    print(Unit(37.7, degree_celcius))
    return 0


if __name__ == "__main__":
    sys.exit(main())
