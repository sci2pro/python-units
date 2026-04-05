# -*- coding: utf-8 -*-
"""Predefined SI base units and common derived units."""

from .unit import DerivedUnit, SIUnit, register_canonical_unit

# SI units
ampere = SIUnit.define('A')
candela = SIUnit.define('cd')
kelvin = SIUnit.define('K')
kilogram = SIUnit.define('kg')
metre = SIUnit.define('m')
mole = SIUnit.define('mol')
second = SIUnit.define('s')

for unit in (ampere, candela, kelvin, kilogram, metre, mole, second):
    register_canonical_unit(unit)

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

for unit in (newton, pascal, joule, watt, coulomb, volt, farad, ohm, siemens, weber, tesla, henry, lumen, lux):
    register_canonical_unit(unit)
