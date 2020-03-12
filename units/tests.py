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

import random
import unittest

from units import *


class TestUnits(unittest.TestCase):
    def test_SIUnits(self):
        """Tests on SI units"""
        rint = random.randint(1, 100)
        self.assertEqual(str(Unit(rint, metre)), '{} m'.format(rint))
        self.assertEqual(str(Unit(rint, second)), '{} s'.format(rint))
        self.assertEqual(str(Unit(rint, kilogram)), '{} kg'.format(rint))
        self.assertEqual(str(Unit(rint, kelvin)), '{} K'.format(rint))
        self.assertEqual(str(Unit(rint, candela)), '{} cd'.format(rint))
        self.assertEqual(str(Unit(rint, ampere)), '{} A'.format(rint))
        self.assertEqual(str(Unit(rint, mole)), '{} mol'.format(rint))

    def test_DerivedUnits(self):
        """Tests on derived units"""
        rint = random.randint(1, 100)
        self.assertEqual(str(Unit(rint, radian)), '{} rad'.format(rint))
        self.assertEqual(str(Unit(rint, steradian)), '{} sr'.format(rint))
        self.assertEqual(str(Unit(rint, hertz)), '{} Hz'.format(rint))
        self.assertEqual(str(Unit(rint, newton)), '{} N'.format(rint))
        self.assertEqual(str(Unit(rint, pascal)), '{} Pa'.format(rint))
        self.assertEqual(str(Unit(rint, joule)), '{} J'.format(rint))
        self.assertEqual(str(Unit(rint, watt)), '{} W'.format(rint))
        self.assertEqual(str(Unit(rint, coulomb)), '{} C'.format(rint))
        self.assertEqual(str(Unit(rint, volt)), '{} V'.format(rint))
        self.assertEqual(str(Unit(rint, farad)), '{} F'.format(rint))
        self.assertEqual(str(Unit(rint, ohm)), '{} Ω'.format(rint))
        self.assertEqual(str(Unit(rint, siemens)), '{} S'.format(rint))
        self.assertEqual(str(Unit(rint, weber)), '{} Wb'.format(rint))
        self.assertEqual(str(Unit(rint, tesla)), '{} T'.format(rint))
        self.assertEqual(str(Unit(rint, henry)), '{} H'.format(rint))
        self.assertEqual(str(Unit(rint, degree_celcius)), '{} °C'.format(rint))
        self.assertEqual(str(Unit(rint, lumen)), '{} lm'.format(rint))
        self.assertEqual(str(Unit(rint, lux)), '{} lx'.format(rint))
        self.assertEqual(str(Unit(rint, becquerel)), '{} Bq'.format(rint))
        self.assertEqual(str(Unit(rint, gray)), '{} Gy'.format(rint))
        self.assertEqual(str(Unit(rint, sievert)), '{} Sv'.format(rint))
        self.assertEqual(str(Unit(rint, katal)), '{} kat'.format(rint))

    def test_Unit(self):
        """Test on the Unit class"""
        rint = random.randint(1, 100)
        x = Unit(rint, metre)
        self.assertEqual(x.value, rint)
        self.assertEqual(str(x.unit), 'm')
        self.assertEqual(str(x.full_units), '{} m'.format(rint))

    def test_scalars(self):
        """Test multiplication or division by a scalar"""
        rint = random.randint(1, 100)
        rint2 = random.randint(1, 100)
        x = Unit(rint, metre)
        y = x * rint2
        z = x / rint2
        self.assertEqual(str(y), '{} m'.format(rint * rint2))
        self.assertEqual(str(z), '{} m'.format(rint / rint2))

    def test_invalid_operations(self):
        """Test operations that would fail e.g. addition of different units"""
        rnum = random.random()
        with self.assertRaises(TypeError):
            complex(Unit(rnum, metre))
        with self.assertRaises(TypeError):
            int(Unit(rnum, metre))
        with self.assertRaises(TypeError):
            float(Unit(rnum, metre))
        # with self.assertRaises(TypeError):
        #     long(Unit(rnum, metre))

    def test_unary_operators(self):
        """Test unary operators"""
        rint = random.randint(1, 100)
        x = Unit(rint, metre)
        y = Unit(-rint, metre)
        self.assertEqual(str(-x), '{} m'.format(-rint))
        self.assertEqual(str(-y), '{} m'.format(rint))
        self.assertEqual(str(+x), '{} m'.format(+rint))
        self.assertEqual(str(+y), '{} m'.format(-rint))
        self.assertEqual(str(abs(x)), '{} m'.format(abs(rint)))
        self.assertEqual(str(abs(y)), '{} m'.format(abs(-rint)))

    def test_operations(self):
        """Test operations of the form Unit <operation> OtherUnit"""
        rnum1 = random.random() * 10
        rnum2 = random.random() * 10
        x = Unit(rnum1, metre)
        y = Unit(rnum2, metre)
        self.assertEqual(str(x + y), '{} m'.format(rnum1 + rnum2))
        self.assertEqual(str(y + x), '{} m'.format(rnum2 + rnum1))

        self.assertEqual(str(x - y), '{} m'.format(rnum1 - rnum2))
        self.assertEqual(str(y - x), '{} m'.format(rnum2 - rnum1))

        self.assertEqual(str(x * y), '{} m^2'.format(rnum1 * rnum2))
        self.assertEqual(str(y * x), '{} m^2'.format(rnum2 * rnum1))

        self.assertEqual(str(x / y), '{}'.format(rnum1 / rnum2))
        self.assertEqual(str(y / x), '{}'.format(rnum2 / rnum1))

        self.assertEqual(str(x // y), '{}'.format(rnum1 // rnum2))
        self.assertEqual(str(y // x), '{}'.format(rnum2 // rnum1))

        self.assertEqual(str(x % y), '{}'.format(rnum1 % rnum2))
        self.assertEqual(str(y % x), '{}'.format(rnum2 % rnum1))

        a, b = divmod(x, y)
        self.assertEqual(str(a), '{}'.format(rnum1 // rnum2))
        self.assertEqual(str(b), '{}'.format(rnum1 % rnum2))

        c, d = divmod(y, x)
        self.assertEqual(str(c), '{}'.format(rnum2 // rnum1))
        self.assertEqual(str(d), '{}'.format(rnum2 % rnum1))

    def test_type_conversions(self):
        """Test conversion functions"""
        rnum = random.random() * 10
        rint = random.randint(1, 100)
        self.assertEqual(str(int_unit(Unit(rnum, metre))), '{} m'.format(int(rnum)))
        self.assertEqual(str(float_unit(Unit(rint, metre))), '{} m'.format(float(rint)))
        # self.assertEqual(str(long_unit(Unit(rnum, metre))), '{} m'.format(long(rnum)))
        self.assertEqual(str(complex_unit(Unit(rnum, metre))), '{} m'.format(complex(rnum)))


if __name__ == "__main__":
    unittest.main()
