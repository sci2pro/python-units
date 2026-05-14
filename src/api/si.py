# -*- coding: utf-8 -*-
"""Predefined SI base units and common derived units."""

from core.unit_definitions import DerivedUnit, SIUnit, register_canonical_unit

ampere = SIUnit.define("A")
candela = SIUnit.define("cd")
kelvin = SIUnit.define("K")
kilogram = SIUnit.define("kg")
metre = SIUnit.define("m")
mole = SIUnit.define("mol")
second = SIUnit.define("s")

for unit in (ampere, candela, kelvin, kilogram, metre, mole, second):
    register_canonical_unit(unit)

radian = DerivedUnit.define("rad", metre / metre)
steradian = DerivedUnit.define("sr", metre * metre / metre / metre)
hertz = DerivedUnit.define("Hz", SIUnit() / second)
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
degree_celcius = DerivedUnit.define(
    "°C",
    kelvin,
    conversion_offset=273.15,
    supports_multiplicative_conversion=False,
)
lumen = DerivedUnit.define("lm", candela * steradian)
lux = DerivedUnit.define("lx", lumen / metre / metre)
becquerel = DerivedUnit.define("Bq", SIUnit() / second)
gray = DerivedUnit.define("Gy", joule / kilogram)
sievert = DerivedUnit.define("Sv", joule / kilogram)
katal = DerivedUnit.define("kat", mole / second)

kilometre = DerivedUnit.define("km", metre, conversion_factor=1000.0)
centimetre = DerivedUnit.define("cm", metre, conversion_factor=0.01)
millimetre = DerivedUnit.define("mm", metre, conversion_factor=0.001)
micrometre = DerivedUnit.define("µm", metre, conversion_factor=0.000001)
nanometre = DerivedUnit.define("nm", metre, conversion_factor=0.000000001)
picometre = DerivedUnit.define("pm", metre, conversion_factor=0.000000000001)

gram = DerivedUnit.define("g", kilogram, conversion_factor=0.001)
milligram = DerivedUnit.define("mg", kilogram, conversion_factor=0.000001)
microgram = DerivedUnit.define("µg", kilogram, conversion_factor=0.000000001)
picogram = DerivedUnit.define("pg", kilogram, conversion_factor=0.000000000000001)
tonne = DerivedUnit.define("t", kilogram, conversion_factor=1000.0)

minute = DerivedUnit.define("min", second, conversion_factor=60.0)
hour = DerivedUnit.define("h", second, conversion_factor=3600.0)
millisecond = DerivedUnit.define("ms", second, conversion_factor=0.001)
microsecond = DerivedUnit.define("µs", second, conversion_factor=0.000001)
nanosecond = DerivedUnit.define("ns", second, conversion_factor=0.000000001)
picosecond = DerivedUnit.define("ps", second, conversion_factor=0.000000000001)

milliampere = DerivedUnit.define("mA", ampere, conversion_factor=0.001)
kiloampere = DerivedUnit.define("kA", ampere, conversion_factor=1000.0)
millivolt = DerivedUnit.define("mV", volt, conversion_factor=0.001)
kilovolt = DerivedUnit.define("kV", volt, conversion_factor=1000.0)
milliwatt = DerivedUnit.define("mW", watt, conversion_factor=0.001)
kilowatt = DerivedUnit.define("kW", watt, conversion_factor=1000.0)
megawatt = DerivedUnit.define("MW", watt, conversion_factor=1000000.0)

for unit in (
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
):
    register_canonical_unit(unit)

__all__ = [
    "ampere",
    "becquerel",
    "candela",
    "centimetre",
    "coulomb",
    "degree_celcius",
    "farad",
    "gram",
    "gray",
    "henry",
    "hertz",
    "hour",
    "joule",
    "katal",
    "kelvin",
    "kilogram",
    "kiloampere",
    "kilometre",
    "kilovolt",
    "kilowatt",
    "lumen",
    "lux",
    "megawatt",
    "metre",
    "microgram",
    "micrometre",
    "microsecond",
    "milliampere",
    "milligram",
    "millimetre",
    "millisecond",
    "millivolt",
    "milliwatt",
    "minute",
    "mole",
    "nanometre",
    "nanosecond",
    "newton",
    "ohm",
    "pascal",
    "picogram",
    "picometre",
    "picosecond",
    "radian",
    "second",
    "siemens",
    "sievert",
    "steradian",
    "tesla",
    "tonne",
    "volt",
    "watt",
    "weber",
]
