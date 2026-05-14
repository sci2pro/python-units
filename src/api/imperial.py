# -*- coding: utf-8 -*-
"""Common imperial and US customary units."""

from api.si import kelvin, kilogram, metre
from core.unit_definitions import DerivedUnit

inch = DerivedUnit.define("in", metre, conversion_factor=0.0254)
foot = DerivedUnit.define("ft", metre, conversion_factor=0.3048)
yard = DerivedUnit.define("yd", metre, conversion_factor=0.9144)
mile = DerivedUnit.define("mi", metre, conversion_factor=1609.344)

ounce = DerivedUnit.define("oz", kilogram, conversion_factor=0.028349523125)
pound = DerivedUnit.define("lb", kilogram, conversion_factor=0.45359237)

fahrenheit = DerivedUnit.define(
    "°F",
    kelvin,
    conversion_factor=5.0 / 9.0,
    conversion_offset=459.67 * 5.0 / 9.0,
    supports_multiplicative_conversion=False,
)

__all__ = [
    "fahrenheit",
    "foot",
    "inch",
    "mile",
    "ounce",
    "pound",
    "yard",
]
