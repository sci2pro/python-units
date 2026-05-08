# units

[![badge.fury.io](https://badge.fury.io/py/python-units.svg)](https://badge.fury.io/py/python-units)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://pypi.org/project/python-units/)
[![Coverage 92%](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](/Users/paulkorir/PycharmProjects/python-units/tests/unit/test_units.py)

# The Price of Unitless Arithmetic

On September 23, 1999, flight controllers expected NASA's Mars Climate Orbiter
to pass behind Mars, fire its engine, and come back into radio contact after
orbit insertion. It never came back. When engineers reviewed the final hours of
flight data, the trajectory was not where the navigation system thought it was:
the spacecraft had approached Mars far lower than planned. The investigation
traced the loss to a unit boundary that software had failed to defend. One side
of the system handled "small forces" data in English units; the navigation side
expected metric units.

That is the kind of bug this package is meant to stop. Without units, the
mistake is just arithmetic:

```python
# A navigation routine expects impulse in newton-seconds.
expected_impulse_ns = 120

# A supplier routine accidentally sends a value in a different force unit.
# The number is still just a number, so Python accepts it.
reported_impulse_other_units = 120

trajectory_impulse = expected_impulse_ns + reported_impulse_other_units
print(trajectory_impulse)  # 240
```

There is nothing in `240` that tells you a spacecraft trajectory may now be
wrong. With units attached, the mismatch stops at the boundary:

```python
from units import CustomUnitBase
from units.dimension import DimensionSystem
from units.si import newton, second

class EnglishImpulseUnit(CustomUnitBase):
    dimension_system = DimensionSystem("english-impulse", ("lbf_s",))

pound_force_second = EnglishImpulseUnit.define("lbf_s")

expected_impulse = 120 * newton * second
reported_impulse = 120 * pound_force_second

trajectory_impulse = expected_impulse + reported_impulse
# UnitCompatibilityError: units mismatch: m·kg·s^-1 and lbf_s
```

That failure is the feature. A bug that would otherwise move through a program
as an ordinary number is stopped before it contaminates mission-critical
calculations.

Background: NASA/JPL describe the Mars Climate Orbiter loss as a navigation
error caused by a failure to translate English units to metric, sending the
spacecraft too close to Mars.

Source: https://en.wikipedia.org/wiki/Mars_Climate_Orbiter

# About

`python-units` is a Python package for unit-aware arithmetic. It provides:
- a `Quantity` type that combines numeric values with unit information
- a registry of SI base and derived units
- algebraic unit manipulation and compatibility checks
- explicit multiplicative conversions between compatible units
- a public API that prioritizes scalar-by-unit construction and SI unit imports
- a migration path from the legacy `Unit` constructor and compatibility helpers
- a Python 3-only codebase with no Python 2 compatibility shims
- a project structure that separates public API, core logic, data models, and utilities
- comprehensive unit tests and documentation

Supported Python versions: 3.10+

Python 2 is not supported.

Project layout:

- public facade: `src/units`
- API exports: `src/api`
- business logic: `src/core`
- data models: `src/models`
- utilities: `src/utils`
- tests: `tests/unit` and `tests/integration`

Preferred API:

```python
from units import Quantity
from units.si import metre, second, newton

distance = 10 * metre
time = 2 * second
speed = distance / time
force = 5 * newton
print(distance)
print(speed)
print(force)
```

The preferred construction style is scalar-by-unit multiplication:

```python
from units.si import metre, second

length = 3 * metre
time = 2 * second
speed = length / time
volume = 5 * metre ** 3
```

Because `**` binds more tightly than `*`, `5 * metre ** 3` is interpreted as
`5 * (metre ** 3)`, which is the intended geometric-unit behavior.

The explicit constructor remains supported and is still the right low-level form
when you want to be fully explicit:

```python
from units import Quantity
from units.si import metre

length = Quantity(3, metre)
```

Legacy API compatibility:

```python
import units as u
print(u.Unit(1, u.metre))
```

The legacy `Unit` constructor remains available as a compatibility alias for
`Quantity` during the migration period. It is deprecated and scheduled for
removal in `1.0.0`, but it remains a true alias until then so existing type
checks keep working. New code should prefer `from units import Quantity` and
`from units.si import ...`.

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
from units.si import metre, second

distance = 3 * metre
time = 2 * second
speed = distance / time
volume = 5 * metre ** 3
```

Still supported when you want the fully explicit constructor form:

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
* `convert`
* `value`
* `unit`
* `multiplier`
* `UnitsError`, `InvalidUnitError`, `InvalidValueError`,
  `UnitCompatibilityError`, `UnitOperandError`

Canonical unit imports:

* `from units.si import metre, second, newton`
* prefixed and scaled units such as `kilometre`, `centimetre`, `gram`,
  `minute`, `hour`, `kilowatt`, and `millivolt`

Legacy compatibility helpers:

* `Unit`
* `long_quantity`
* `int_unit`
* `float_unit`
* `long_unit`
* `complex_unit`

These names remain available during the migration period and emit
`DeprecationWarning` when called. `Unit` remains a true alias for `Quantity` and
does not emit a call-time warning, because preserving `Unit is Quantity` is part
of the pre-`1.0.0` compatibility contract. New code should prefer `Quantity`,
scalar-by-unit construction, and the `*_quantity` conversion helpers. The
deprecated compatibility paths are scheduled for removal in `1.0.0`.

# Notes on semantics

* Addition and subtraction require identical units.
* Multiplication and division combine units algebraically.
* Explicit scale-only conversions are available through `quantity.to(unit)` and
  `convert(quantity, unit)`.
* Integer powers of units and unit-bearing quantities are supported.
* Unitless quantities are supported explicitly.
* Affine conversions, such as `degree_celcius <-> kelvin`, are intentionally not
  implemented yet.
* The core quantity model allows signed values. Domain-specific constraints such
  as non-negative lengths should be enforced by higher-level types or validators.

# Conversion foundations

`0.4.0` adds explicit multiplicative conversions. Conversion never happens
silently during addition or subtraction; you choose the target unit.

```python
from units import convert, multiplier, unit, value
from units.si import gram, hour, kilogram, kilometre, metre, minute, second

distance = 1.5 * kilometre
print(distance.to(metre))           # 1500 m
print(convert(2500 * metre, kilometre))  # 2.5 km

duration = 2 * hour
print(duration.to(minute))          # 120 min
print((1500 * gram).to(kilogram))   # 1.5 kg

speed = (72 * kilometre) / (2 * hour)
print(speed)                        # 10.0 m·s^-1

print(value(distance))              # 1.5
print(unit(distance))               # km
print(multiplier(kilometre))        # 1000.0
```

The conversion model is scale-only in this release. Celsius is a named
temperature unit, but converting between Celsius and kelvin requires an offset
and is reserved for a later affine-conversion release.

# Prefixed and scaled units

Common SI prefixes and practical time units are available from `units.si`:

```python
from units.si import (
    centimetre,
    gram,
    hour,
    kiloampere,
    kilometre,
    kilovolt,
    kilowatt,
    megawatt,
    micrometre,
    microsecond,
    milliampere,
    milligram,
    millimetre,
    millisecond,
    millivolt,
    milliwatt,
    minute,
    nanometre,
    nanosecond,
    tonne,
)
```

Scaled units participate correctly in multiplication, division, and powers:

```python
from units.si import hour, kilometre, metre

area = (2 * kilometre) * (3 * metre)
print(area)                         # 6000 m^2

square = (2 * kilometre) ** 2
print(square)                       # 4000000 m^2

speed = (72 * kilometre) / (2 * hour)
print(speed)                        # 10.0 m·s^-1
```

# Familiar composite units

Composite unit expressions such as `kilometre / hour` are algebraic unit
definitions. They carry the correct scale factor, but anonymous composite units
render in canonical SI base form:

```python
from units.si import hour, kilometre

speed = 30 * kilometre / hour
print(speed)                        # 8.333333333333334 m·s^-1
```

When you want a semantically familiar display unit, give that composite unit an
explicit name and convert to it:

```python
from units import DerivedUnit, convert
from units.si import hour, kilometre

kilometres_per_hour = DerivedUnit.define("km·hr^-1", kilometre / hour)

speed = 30 * kilometre / hour
print(convert(speed, kilometres_per_hour))  # 30 km·hr^-1
print(30 * kilometres_per_hour)             # 30 km·hr^-1
```

This keeps the arithmetic deterministic while letting application code choose
domain-specific display names such as `km·hr^-1`, `N·m`, or any other familiar
derived unit form.

# Real-world examples

## Electrical engineering: from resistance to power dissipation

```python
from units.si import ampere, ohm, volt, watt

current = 12 * ampere
resistance = 8 * ohm
voltage = current * resistance
power = voltage * current

print(voltage)  # 96 V
print(power)    # 1152 W
```

This works because the package canonicalizes unambiguous derived-unit assemblies:

- `ampere * ohm -> volt`
- `volt * ampere -> watt`

## Pump sizing: hydraulic power from pressure rise and flow rate

```python
from units.si import metre, second, kilogram, pascal, watt

density = 998 * (kilogram / metre ** 3)
flow_velocity = 2.5 * (metre / second)
pipe_area = 0.0314 * metre ** 2
pressure_rise = 180000 * pascal

volumetric_flow = flow_velocity * pipe_area
hydraulic_power = pressure_rise * volumetric_flow

print(volumetric_flow)   # m^3·s^-1
print(hydraulic_power)   # W
```

This is a good example of a multi-step engineering computation that still renders
to intuitive derived units at the end of the chain.

## Structural mechanics: work from force over distance

```python
from units.si import metre, newton

force = 4200 * newton
displacement = 0.35 * metre
work = force * displacement

print(work)  # J
```

## Geometric quantities: powers of units

```python
from units.si import metre

volume = 5 * metre ** 3
area = (12 * metre) ** 2

print(volume)  # 5 m^3
print(area)    # 144 m^2
```

The unit form is also valid on its own:

```python
from units.si import metre

area_unit = metre ** 2
volume_unit = metre ** 3
```

## Fluid mechanics: dynamic pressure

```python
from units.si import kilogram, metre, pascal, second

density = 1.225 * (kilogram / metre ** 3)
velocity = 68 * (metre / second)
dynamic_pressure = 0.5 * density * velocity * velocity

print(dynamic_pressure)  # Pa
```

## Custom unit systems

Custom unit systems are supported, but they are intentionally separate from SI
canonicalization. Use them when you want the same algebra and formatting
behaviour without forcing your units into the SI registry.

```python
from units import CustomUnitBase, DimensionSystem

class CommUnit(CustomUnitBase):
    dimension_system = DimensionSystem('comm', ('b', 's', 'B'))

bit = CommUnit.define('b')
second = CommUnit.define('s')

data = 32 * bit
duration = 4 * second
rate = data / duration

print(rate)  # 8.0 b·s^-1
```

Custom systems inherit useful behaviour:

- dimensional algebra
- string rendering
- incompatibility checks within a system

They do not automatically simplify into SI-derived names such as `V`, `J`, or
`Pa`, and they cannot be mixed with SI units unless you build an explicit bridge.
