#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
units.tests
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
"""
from __future__ import division, print_function

__author__ = "Paul K. Korir, PhD"
__email__ = "paul.korir@gmail.com"
__date__ = "2017-06-02"

import unittest

import units.si as si
from units import *
from units.errors import (
    InvalidUnitError,
    InvalidValueError,
    UnitCompatibilityError,
    UnitOperandError,
)


class TestUnits(unittest.TestCase):
    def test_new_api_imports(self):
        """Tests the preferred public API."""
        distance = Quantity(3, si.metre)
        time = Quantity(2, si.second)
        force = Quantity(5, si.newton)

        self.assertEqual(str(distance), '3 m')
        self.assertEqual(str(time), '2 s')
        self.assertEqual(str(force), '5 N')
        self.assertEqual(str(distance / time), '1.5 m·s^-1')

    def test_legacy_api_compatibility(self):
        """Tests that the legacy API remains available."""
        self.assertIs(Unit, Quantity)
        self.assertIs(metre, si.metre)
        self.assertIs(second, si.second)
        self.assertIs(newton, si.newton)

    def test_SIUnits(self):
        """Tests on SI units"""
        value = 7
        self.assertEqual(str(Unit(value, metre)), '{} m'.format(value))
        self.assertEqual(str(Unit(value, second)), '{} s'.format(value))
        self.assertEqual(str(Unit(value, kilogram)), '{} kg'.format(value))
        self.assertEqual(str(Unit(value, kelvin)), '{} K'.format(value))
        self.assertEqual(str(Unit(value, candela)), '{} cd'.format(value))
        self.assertEqual(str(Unit(value, ampere)), '{} A'.format(value))
        self.assertEqual(str(Unit(value, mole)), '{} mol'.format(value))

    def test_DerivedUnits(self):
        """Tests on derived units"""
        value = 7
        self.assertEqual(str(Unit(value, radian)), '{} rad'.format(value))
        self.assertEqual(str(Unit(value, steradian)), '{} sr'.format(value))
        self.assertEqual(str(Unit(value, hertz)), '{} Hz'.format(value))
        self.assertEqual(str(Unit(value, newton)), '{} N'.format(value))
        self.assertEqual(str(Unit(value, pascal)), '{} Pa'.format(value))
        self.assertEqual(str(Unit(value, joule)), '{} J'.format(value))
        self.assertEqual(str(Unit(value, watt)), '{} W'.format(value))
        self.assertEqual(str(Unit(value, coulomb)), '{} C'.format(value))
        self.assertEqual(str(Unit(value, volt)), '{} V'.format(value))
        self.assertEqual(str(Unit(value, farad)), '{} F'.format(value))
        self.assertEqual(str(Unit(value, ohm)), '{} Ω'.format(value))
        self.assertEqual(str(Unit(value, siemens)), '{} S'.format(value))
        self.assertEqual(str(Unit(value, weber)), '{} Wb'.format(value))
        self.assertEqual(str(Unit(value, tesla)), '{} T'.format(value))
        self.assertEqual(str(Unit(value, henry)), '{} H'.format(value))
        self.assertEqual(str(Unit(value, degree_celcius)), '{} °C'.format(value))
        self.assertEqual(str(Unit(value, lumen)), '{} lm'.format(value))
        self.assertEqual(str(Unit(value, lux)), '{} lx'.format(value))
        self.assertEqual(str(Unit(value, becquerel)), '{} Bq'.format(value))
        self.assertEqual(str(Unit(value, gray)), '{} Gy'.format(value))
        self.assertEqual(str(Unit(value, sievert)), '{} Sv'.format(value))
        self.assertEqual(str(Unit(value, katal)), '{} kat'.format(value))

    def test_Unit(self):
        """Test on the Unit class"""
        x = Unit(11, metre)
        self.assertEqual(x.value, 11)
        self.assertEqual(str(x.unit), 'm')
        self.assertEqual(str(x.full_units), '11 m')
        self.assertFalse(x.is_unitless)

    def test_scalars(self):
        """Test multiplication or division by a scalar"""
        x = Unit(12, metre)
        y = x * 4
        z = x / 3
        self.assertEqual(str(y), '48 m')
        self.assertEqual(str(z), '4.0 m')
        self.assertEqual(str(24 / x), '2.0 m^-1')
        self.assertEqual(str(24 // x), '2 m^-1')
        self.assertEqual(str(25 % x), '1 m^-1')

    def test_invalid_operations(self):
        """Test operations that would fail e.g. addition of different units"""
        with self.assertRaises(TypeError):
            complex(Unit(1.5, metre))
        with self.assertRaises(TypeError):
            int(Unit(1.5, metre))
        with self.assertRaises(TypeError):
            float(Unit(1.5, metre))
        with self.assertRaises(UnitCompatibilityError):
            Unit(2, metre) + Unit(3, second)
        with self.assertRaises(UnitCompatibilityError):
            Unit(2, metre) % Unit(3, second)
        with self.assertRaises(UnitOperandError):
            Unit(2, metre) + 3
        with self.assertRaises(UnitOperandError):
            3 + Unit(2, metre)
        with self.assertRaises(UnitOperandError):
            Unit(2, metre) * object()
        with self.assertRaises(UnitOperandError):
            Unit(2, metre) // complex(2, 1)
        with self.assertRaises(InvalidValueError):
            Unit('3', metre)
        with self.assertRaises(InvalidUnitError):
            Unit(3, 'metre')

    def test_unary_operators(self):
        """Test unary operators"""
        x = Unit(9, metre)
        y = Unit(-9, metre)
        self.assertEqual(str(-x), '-9 m')
        self.assertEqual(str(-y), '9 m')
        self.assertEqual(str(+x), '9 m')
        self.assertEqual(str(+y), '-9 m')
        self.assertEqual(str(abs(x)), '9 m')
        self.assertEqual(str(abs(y)), '9 m')

    def test_operations(self):
        """Test operations of the form Unit <operation> OtherUnit"""
        x = Unit(9.0, metre)
        y = Unit(4.0, metre)
        self.assertEqual(str(x + y), '13.0 m')
        self.assertEqual(str(y + x), '13.0 m')

        self.assertEqual(str(x - y), '5.0 m')
        self.assertEqual(str(y - x), '-5.0 m')

        self.assertEqual(str(x * y), '36.0 m^2')
        self.assertEqual(str(y * x), '36.0 m^2')

        self.assertEqual(str(x / y), '2.25')
        self.assertEqual(str(y / x), '0.4444444444444444')

        self.assertEqual(str(x // y), '2.0')
        self.assertEqual(str(y // x), '0.0')

        self.assertEqual(str(x % y), '1.0 m')
        self.assertEqual(str(y % x), '4.0 m')

        a, b = divmod(x, y)
        self.assertEqual(str(a), '2.0')
        self.assertEqual(str(b), '1.0 m')

        c, d = divmod(y, x)
        self.assertEqual(str(c), '0.0')
        self.assertEqual(str(d), '4.0 m')

    def test_type_conversions(self):
        """Test conversion functions"""
        self.assertEqual(str(int_unit(Unit(4.8, metre))), '4 m')
        self.assertEqual(str(float_unit(Unit(7, metre))), '7.0 m')
        self.assertEqual(str(long_unit(Unit(4.8, metre))), '4 m')
        self.assertEqual(str(complex_unit(Unit(4.8, metre))), '(4.8+0j) m')
        self.assertEqual(str(int_quantity(Quantity(4.8, metre))), '4 m')
        self.assertEqual(str(float_quantity(Quantity(7, metre))), '7.0 m')

    def test_operation_derived(self):
        """Operations on derived units"""
        v1 = Unit(6.0, newton)
        v2 = Unit(2.0, radian)
        result = v1 / v2
        self.assertIsInstance(str(result), str) # otherwise we get a typeerror
        self.assertEqual(result.full_units, '3.0 m·kg·s^-2')

    def test_reverse_unit_operations(self):
        """Test reverse operations between two Unit objects."""
        x = Unit(5, metre)
        y = Unit(14, metre)
        self.assertEqual(str(y - x), '9 m')
        self.assertEqual(str(y / x), '2.8')

    def test_unitless_values(self):
        """Test behavior for dimensionless values."""
        unitless = Unit(3)
        self.assertTrue(unitless.is_unitless)
        self.assertEqual(str(unitless), '3')
        self.assertEqual(str(unitless * Unit(2, metre)), '6 m')
        self.assertEqual(str(Unit(2, metre) / unitless), '0.6666666666666666 m')

    def test_setters_and_definitions(self):
        """Test explicit validation in setters and unit definitions."""
        x = Unit(3, metre)
        x.value = 4.5
        x.unit = second
        self.assertEqual(str(x), '4.5 s')

        with self.assertRaises(InvalidValueError):
            x.value = 'invalid'
        with self.assertRaises(InvalidUnitError):
            x.unit = 'invalid'
        with self.assertRaises(InvalidUnitError):
            SIUnit.define('invalid')
        with self.assertRaises(InvalidValueError):
            SIUnit.define('m', 1.2)

    def test_helper_rejects_invalid_operand(self):
        """Test helper conversion functions reject non-Unit operands."""
        with self.assertRaises(UnitOperandError):
            int_unit(3)
        with self.assertRaises(UnitOperandError):
            float_unit(3)
        with self.assertRaises(UnitOperandError):
            long_unit(3)
        with self.assertRaises(UnitOperandError):
            complex_unit(3)


if __name__ == "__main__":
    unittest.main()
