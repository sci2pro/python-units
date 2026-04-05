# units

[![badge.fury.io](https://badge.fury.io/py/python-units.svg)](https://badge.fury.io/py/python-units)

Python library to represent quantities with units

Supported Python versions: 3.10+

Python 2 is not supported.

Preferred API:

```python
from units import Quantity
from units.si import metre, second, newton

distance = Quantity(10, metre)
time = Quantity(2, second)
speed = distance / time
force = Quantity(5, newton)
print(distance)
print(speed)
print(force)
```

Legacy API compatibility:

```python
import units as u
print(u.Unit(1, u.metre))
```

The legacy `Unit` constructor remains available as a compatibility alias for
`Quantity` during the migration period, but new code should prefer
`from units import Quantity` and `from units.si import ...`.

The package is Python 3-only. Python 2 compatibility behavior is not part of the
supported interface.

# Migration guide

Old style:

```python
import units as u
distance = u.Unit(3, u.metre)
time = u.Unit(2, u.second)
speed = distance / time
```

New style:

```python
from units import Quantity
from units.si import metre, second

distance = Quantity(3, metre)
time = Quantity(2, second)
speed = distance / time
```

# Public API

Stable top-level imports:

* `Quantity`
* `Unit` (compatibility alias for `Quantity`)
* `UnitsError`, `InvalidUnitError`, `InvalidValueError`,
  `UnitCompatibilityError`, `UnitOperandError`

Canonical unit imports:

* `from units.si import metre, second, newton`

Legacy compatibility helpers:

* `long_quantity`
* `long_unit`

These names remain available as compatibility aliases for integer conversion in
Python 3, but new code should prefer `int_quantity`.

# Notes on semantics

* Addition and subtraction require identical units.
* Multiplication and division combine units algebraically.
* Unitless quantities are supported explicitly.
* The core quantity model allows signed values. Domain-specific constraints such
  as non-negative lengths should be enforced by higher-level types or validators.

# Upcoming features
* Short and long units (currently only short units)

* Multipliers e.g. kilo (k), mega (M), kibi (KiB), ergs etc.

* Arbitrary units e.g. bits (b), cars etc.

# Features
* Basic units

```python
import units as u
from random import randint
# ampere
print(u.Quantity(randint(1, 100), u.ampere))
# candela
print(u.Quantity(randint(1, 100), u.candela))
# kelvin
print(u.Quantity(randint(1, 100), u.kelvin))
# kilogram
print(u.Quantity(randint(1, 100), u.kilogram))
# metre
print(u.Quantity(randint(1, 100), u.metre))
# mole
print(u.Quantity(randint(1, 100), u.mole))
# second
print(u.Quantity(randint(1, 100), u.second))
```

* Operations on units

```python
import units as u
from random import random
x = u.Quantity(random(), u.second)
y = u.Quantity(random(), u.ampere)
# addition
print(x + y)
print(y + x)
# subtraction
print(x - y)
print(y - x)
# multiplication
print(x * y)
print(y * x)
# division/true division
print(x / y)
print(y / x)
# floor division
print(x // y)
print(y // x)
# modulus
print(x % y)
# power
print(x ** y)
print(y ** x)
```

* Operations between scalars and units

```python
import units as u
from random import random
x = u.Quantity(random(), u.second)
a = random() * 10
# addition
print(a + y)
print(y + a)
# subtraction
print(a - y)
print(y - a)
# multiplication
print(a * y)
print(y * a)
# division/true division
print(a / y)
print(y / a)
# floor division
print(a // y)
print(y // a)
# modulus
print(a % y)
# power
print(a ** y)
print(y ** a)
```

* Derived units

```python
import units as u
from random import random
# hertz
print(u.Quantity(random() * 10, u.hertz))
# newton
print(u.Quantity(random() * 10, u.newton))
# pascal
print(u.Quantity(random() * 10, u.pascal))
# joule
print(u.Quantity(random() * 10, u.joule))
# watt
print(u.Quantity(random() * 10, u.watt))
# coulomb
print(u.Quantity(random() * 10, u.coulomb))
# volt
print(u.Quantity(random() * 10, u.volt))
# farad
print(u.Quantity(random() * 10, u.farad))
# ohm
print(u.Quantity(random() * 10, u.ohm))
# siemems
print(u.Quantity(random() * 10, u.siemens))
# weber
print(u.Quantity(random() * 10, u.weber))
# tesla
print(u.Quantity(random() * 10, u.tesla))
# henry
print(u.Quantity(random() * 10, u.henry))
# degree celcius
print(u.Quantity(random() * 10, u.degree_celcius))
# lumen
print(u.Quantity(random() * 10, u.lumen))
# lux
print(u.Quantity(random() * 10, u.lux))
# becquerel
print(u.Quantity(random() * 10, u.becquerel))
# gray
print(u.Quantity(random() * 10, u.gray))
# sievert
print(u.Quantity(random() * 10, u.sievert))
# katal
print(u.Quantity(random() * 10, u.katal))
```

* Unpacking derived units

```python
import units as u
from random import random
# hertz
print(u.Quantity(random() * 10, u.hertz).full_units)
# newton
print(u.Quantity(random() * 10, u.newton).full_units)
# pascal
print(u.Quantity(random() * 10, u.pascal).full_units)
# joule
print(u.Quantity(random() * 10, u.joule).full_units)
# watt
print(u.Quantity(random() * 10, u.watt).full_units)
# coulomb
print(u.Quantity(random() * 10, u.coulomb).full_units)
# volt
print(u.Quantity(random() * 10, u.volt).full_units)
# farad
print(u.Quantity(random() * 10, u.farad).full_units)
# ohm
print(u.Quantity(random() * 10, u.ohm).full_units)
# siemems
print(u.Quantity(random() * 10, u.siemens).full_units)
# weber
print(u.Quantity(random() * 10, u.weber).full_units)
# tesla
print(u.Quantity(random() * 10, u.tesla).full_units)
# henry
print(u.Quantity(random() * 10, u.henry).full_units)
# degree celcius
print(u.Quantity(random() * 10, u.degree_celcius).full_units)
# lumen
print(u.Quantity(random() * 10, u.lumen).full_units)
# lux
print(u.Quantity(random() * 10, u.lux).full_units)
# becquerel
print(u.Quantity(random() * 10, u.becquerel).full_units)
# gray
print(u.Quantity(random() * 10, u.gray).full_units)
# sievert
print(u.Quantity(random() * 10, u.sievert).full_units)
# katal
print(u.Quantity(random() * 10, u.katal).full_units)
```

* Arbitrary derived units

```python
import units as u
speed = u.DerivedUnit.define('speed', u.metre / u.second)
v = u.Quantity(10, speed)
```

* Arbitrary custom units

```python
import units as u
from units import BaseUnit

class CommUnit(BaseUnit):
    """Template class for communication units"""
    def __init__(self, *args, **kwargs):
        super(CommUnit, self).__init__(*args, **kwargs)
        # redefine the base units
        self.unit_dict = {
            'b': 0,
            's': 0,
            'B': 0,
        }
    @classmethod
    def define(cls, key, value=1):
    	"""Constructor"""
        obj = cls()
        assert key in obj.unit_dict.keys()
        assert isinstance(value, int)
        obj.unit_dict[key] = value
        return obj
```

which will be used as follows

```python
bit = CommUnit.define('b') # define a bit as referring to the 'b' unit
second = CommUnit.define('s') # a second is 's'
data = u.Quantity(32, bit)
T = u.Quantity(4, second)
# data rate
print(data / T) # 8.0 b·s^-1 - bits per second
```
