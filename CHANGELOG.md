# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-04-06

### Release notes

`0.2.0` is the first release in the modernized API line.

This release keeps legacy code working while introducing a clearer and more ergonomic public API, a stronger internal architecture, and a modern Python-only packaging and test workflow.

The preferred API is now:

```python
from units import Quantity
from units.si import metre, second, newton

distance = 10 * metre
time = 2 * second
speed = distance / time
force = 5 * newton
```

The explicit constructor remains fully supported:

```python
distance = Quantity(10, metre)
```

Legacy compatibility is still preserved in this release:

```python
import units as u
distance = u.Unit(10, u.metre)
```

### Added

- `Quantity` as the preferred quantity type
- `units.si` as the canonical import location for SI and derived units
- scalar-by-unit construction, such as `3 * metre`
- exponent support for units and quantities, such as `5 * metre ** 3`
- immutable `Dimension` and `DimensionSystem` models
- registry-backed canonicalization for unambiguous SI derived units
- support for custom unit systems through `CustomUnitBase`
- GitHub Actions CI and publishing workflows
- `pyproject.toml` packaging metadata
- `pytest`-based unit tests and integration tests
- layered source structure under `src/api`, `src/core`, `src/models`, and `src/utils`
- contributor guidance and an explicit project plan

### Changed

- the package is now Python 3-only
- the preferred construction style is now scalar-by-unit multiplication instead of always calling `Quantity(...)`
- the runtime package has been refactored into a layered architecture while preserving the `units` facade
- documentation is now centered on `README.md` with real-world engineering examples
- test and build workflows now reflect the `src` layout and modern Python packaging

### Fixed

- explicit typed validation replaced `assert`-based validation
- fragile arithmetic paths and unsupported operand handling were corrected
- reverse arithmetic and dimensionless handling were tightened
- custom unit systems were restored after the dimensional refactor and kept separate from SI canonicalization

### Compatibility

- `Unit` remains available as a compatibility alias for `Quantity`
- top-level unit exports remain available during the transition
- legacy helper names such as `long_unit` and `long_quantity` still exist for compatibility
- deprecation warnings are not yet emitted in this release

### Current state

As of `0.2.0`, the project has the following characteristics:

- public facade in `src/units`
- layered implementation in `src/api`, `src/core`, `src/models`, and `src/utils`
- intentionally empty `src/services` and `src/adapters` packages reserved for future growth
- Python `3.10+` support
- `pytest` unit and integration coverage
- current verified total coverage of `92%`
- preferred API based on `3 * metre` style quantity construction
- explicit constructor support retained through `Quantity(value, unit)`
- legacy API still available for migration

### Next steps after 0.2.0

- implement compatibility deprecation policy
- add low-noise warnings for legacy aliases
- define removal timing for legacy paths in a future breaking release

