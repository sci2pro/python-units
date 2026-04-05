# units

[![badge.fury.io](https://badge.fury.io/py/python-units.svg)](https://badge.fury.io/py/python-units)

Python library to represent quantities with units.

Supported Python versions: 3.10+

Python 2 is not supported.

Project layout:

- runtime package: `src/units`
- tests: `tests/unit`

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
* Integer powers of units and unit-bearing quantities are supported.
* Unitless quantities are supported explicitly.
* The core quantity model allows signed values. Domain-specific constraints such
  as non-negative lengths should be enforced by higher-level types or validators.

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
