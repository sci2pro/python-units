# -*- coding: utf-8 -*-
"""Public API for the units package.

Preferred usage:

    from units import Quantity
    from units.si import metre, second
"""

import sys

from .errors import (
    InvalidUnitError,
    InvalidValueError,
    UnitCompatibilityError,
    UnitOperandError,
    UnitsError,
)
from .dimension import Dimension, DimensionSystem
from .quantity import (
    Quantity,
    complex_quantity,
    complex_unit,
    float_quantity,
    float_unit,
    int_quantity,
    int_unit,
    long_quantity,
    long_unit,
)
from .si import (
    ampere,
    becquerel,
    candela,
    coulomb,
    degree_celcius,
    farad,
    gray,
    henry,
    hertz,
    joule,
    katal,
    kelvin,
    kilogram,
    lumen,
    lux,
    metre,
    mole,
    newton,
    ohm,
    pascal,
    radian,
    second,
    siemens,
    sievert,
    steradian,
    tesla,
    volt,
    watt,
    weber,
)
from .unit import BaseUnit, CustomUnitBase, DerivedUnit, SIUnit

__author__ = "Paul K. Korir"
__email__ = "paul.korir@gmail.com"
__date__ = "2017-06-01"

# Legacy compatibility alias. New code should use Quantity.
Unit = Quantity

__all__ = [
    'ampere',
    'BaseUnit',
    'becquerel',
    'candela',
    'complex_quantity',
    'complex_unit',
    'coulomb',
    'CustomUnitBase',
    'degree_celcius',
    'DerivedUnit',
    'farad',
    'float_quantity',
    'float_unit',
    'gray',
    'henry',
    'hertz',
    'int_quantity',
    'int_unit',
    'InvalidUnitError',
    'InvalidValueError',
    'joule',
    'katal',
    'kelvin',
    'kilogram',
    'long_quantity',
    'long_unit',
    'lumen',
    'lux',
    'metre',
    'mole',
    'newton',
    'ohm',
    'pascal',
    'Quantity',
    'radian',
    'second',
    'SIUnit',
    'siemens',
    'sievert',
    'steradian',
    'tesla',
    'Unit',
    'UnitCompatibilityError',
    'UnitOperandError',
    'UnitsError',
    'volt',
    'watt',
    'weber',
]


def main():
    """Legacy demo entry point."""
    x = Quantity(1, metre)
    y = Quantity(2, metre)
    print(x)
    print(x + y)
    print(x * y)
    print(x / y)
    z = Quantity(3, second)
    print(x / z)
    i = Quantity(5.7, ampere)
    print(z * i)
    print(Quantity(272.93, kilogram * metre / second / second))
    print(Quantity(20.232, kilogram * metre * metre / second / second / ampere))
    print(
        Quantity(272.93, kilogram * metre / second / second)
        * Quantity(20.232, kilogram * metre * metre / second / second / ampere)
    )
    k = Quantity(392.22, hertz)
    print(k)
    print(k.full_units)
    j = Quantity(29302.33, SIUnit() / second)
    print(j)
    F = Quantity(93.39, newton)
    print(F)
    print(F.full_units)
    P = Quantity(758, pascal)
    print(P)
    print(P.full_units)
    print(Quantity(93, becquerel).full_units)
    print(Quantity(20, katal).full_units)
    print(2 * Quantity(30, metre))
    print(2 / Quantity(20, metre))
    print(Quantity(20, metre) / 2)
    print(Quantity(37.7, degree_celcius))
    return 0


if __name__ == "__main__":
    sys.exit(main())
    'Dimension',
    'DimensionSystem',
