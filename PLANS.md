# PLANS.md

## Purpose

This repository implements a pure-Python library for representing quantities with units, preserving dimensional correctness during arithmetic, and rendering results using SI base or preferred derived units.

The preferred public API is:

```python
from units import Quantity
from units.si import metre, second, newton
```

The package also preserves a temporary legacy compatibility path through `Unit = Quantity` and top-level unit re-exports.

## Current State

The repository has already completed a substantial transition from the original flat package:

- runtime package code lives in `src/units`
- layered implementation now lives in `src/api`, `src/core`, `src/models`, and `src/utils`
- tests live in `tests/unit`
- integration tests live in `tests/integration`
- packaging is managed through `pyproject.toml`
- CI and publish workflows exist under `.github/workflows`
- the public API is typed
- scalar-by-unit construction is supported as the preferred quantity-construction style
- the dimensional model uses immutable `Dimension` objects
- SI canonicalization is registry-backed
- custom unit systems are supported through `DimensionSystem` and `CustomUnitBase`
- the README is now the primary user-facing documentation

The implementation is coherent in purpose and significantly improved over the original package. The main remaining gaps are now policy and lifecycle concerns rather than core structure.

## Alignment With `AGENTS.md`

### Already aligned

- deterministic arithmetic and explicit failure behavior
- minimal runtime dependencies
- typed public interfaces
- dedicated error module
- Python 3-only packaging policy
- `src` plus `tests` repository layout
- layered implementation structure under `src/api`, `src/core`, `src/models`, and `src/utils`
- `pytest`-driven unit and integration test suites
- CI-based build and test verification

### Still not aligned

- compatibility aliases remain but do not emit deprecation warnings

### Intentionally empty layers

`src/services` and `src/adapters` are intentionally present but empty.

That is acceptable for this library today because:

- there is no orchestration layer distinct from the core unit algebra
- there are no external integrations, I/O boundaries, or replaceable infrastructure adapters

Those packages should remain available for future growth, but they are not an active gap.

## Architectural Direction

The target architecture should preserve the current public API while reorganizing the implementation to match `AGENTS.md`.

### Public API to preserve

```python
from units import Quantity
from units.si import metre, second, newton
```

Compatibility to preserve during the transition:

- `Unit` as an alias for `Quantity`
- top-level re-exports such as `metre`, `second`, and `newton`
- legacy conversion helpers until a deliberate breaking release

### Preferred quantity-construction style

The package should support two coherent quantity-construction paths:

```python
length = Quantity(3, metre)
length = 3 * metre
```

The explicit constructor should remain available as the low-level, fully explicit form.

The preferred ergonomic form should become scalar-by-unit multiplication, because it is more natural for engineering and scientific calculations and reads more clearly in longer expressions.

Design rule:

- `scalar * unit -> Quantity`
- `unit * scalar -> Quantity`
- `unit * unit -> unit definition`
- `quantity * unit -> Quantity`
- `quantity / unit -> Quantity`

Planning implication:

- unit definitions should behave as multiplicative basis elements with conceptual magnitude `1`
- the README should eventually prefer examples such as `3 * metre` over `Quantity(3, metre)`
- the naming distinction between `Quantity` and unit-definition classes remains important

### Core model to preserve

- `DimensionSystem`: defines an ordered base-dimension family
- `Dimension`: immutable exponent tuple within a `DimensionSystem`
- `Unit` definitions: `SIUnit`, `DerivedUnit`, `CustomUnitBase`
- `Quantity`: numeric value paired with a unit definition
- canonical SI resolution for unambiguous derived dimensions

### Semantic policy to preserve

- dimensional correctness belongs in the core model
- domain constraints such as non-negative length belong in higher-level types or validators, not in the base `Quantity` type
- SI canonicalization should remain strong and deterministic
- custom unit systems should stay easy to define but separate from SI canonicalization

## Revised Phase Status

### Completed Phase 1: Correctness and contract hardening

Completed work:

- replaced `assert`-based validation with explicit typed errors
- corrected fragile arithmetic paths
- normalized dimensionless handling
- expanded automated tests for success and failure cases

### Completed Phase 2: Public API transition

Completed work:

- introduced `Quantity` as the preferred value type
- added `units.si`
- kept `Unit` as a compatibility alias
- split implementation across focused modules
- added scalar-by-unit construction so expressions such as `3 * metre` create `Quantity` objects
- added exponent support for unit and quantity expressions such as `5 * metre ** 3`

### Completed Phase 3: CI/CD and Python 3 packaging

Completed work:

- added GitHub Actions CI and publish workflows
- moved packaging metadata into `pyproject.toml`
- dropped Python 2 from supported packaging and CI policy

### Completed Phase 4: Interface clarity and documentation

Completed work:

- added typing to the public API
- made `README.md` the main documentation
- documented migration from the legacy API
- added real-world usage examples

### Completed Phase 5: Dimensional architecture redesign

Completed work:

- introduced immutable `Dimension` and `DimensionSystem`
- added registry-backed SI canonicalization
- restored support for custom unit systems without weakening the SI path

### Completed Phase 6: Repository layout baseline

Completed work:

- migrated runtime code to `src/units`
- migrated tests to `tests/unit`
- updated packaging and CI to the new layout

This is the current baseline. Remaining phases now focus on closing the gap between that baseline and the stricter `AGENTS.md` structure.

## Remaining Phases

### Completed Phase 7: Layered package restructuring

Completed work:

- introduced `src/core` for quantity logic, unit algebra, and error types
- introduced `src/models` for immutable dimension types
- introduced `src/api` for curated exports and SI definitions
- introduced `src/utils` for reusable numeric helpers
- preserved `src/units` as a thin public compatibility facade
- added placeholder `src/services` and `src/adapters` packages to satisfy the repository structure

### Completed Phase 8: Testing and verification alignment

Completed work:

- rewrote the unit tests in `pytest` style
- introduced `tests/integration`
- added integration coverage for public imports and compatibility behavior
- updated CI and tox to run both test layers

### Phase 9: Compatibility deprecation policy

Goal:

Honor the migration plan deliberately instead of keeping compatibility aliases indefinitely.

Required changes:

- add low-noise deprecation warnings for `Unit` and legacy helpers where appropriate
- add tests for warning behavior
- publish removal criteria in the README and release notes
- decide the target breaking release for removal of deprecated paths

Recommended release sequence:

1. Keep compatibility aliases in the next transition release.
2. Introduce warnings once the layered architecture is stable.
3. Remove deprecated paths only in a deliberate breaking release.

### Phase 10: Higher-level domain extensions

Goal:

Add optional higher-level semantics without weakening the core model.

Candidate work:

- constrained domain types such as `Length`, `Distance`, or `Duration`
- explicit conversion APIs
- richer canonicalization policies
- more engineering and scientific examples

This phase is optional and should not start until the compatibility policy is settled.

## Immediate Priorities

The next implementation work should happen in this order:

1. Phase 9: deprecation policy implementation
2. Phase 10: higher-level domain extensions, only if they are still wanted after the compatibility policy is settled

## Definition of Done For The Remaining Plan

The plan is complete only when all of the following are true:

- the repository structure materially matches `AGENTS.md`
- public interfaces remain typed and documented
- tests are primarily `pytest`-based and include integration coverage
- deprecation behavior is explicit and documented
- demo behavior has been removed from runtime modules
- the README reflects the actual supported API and migration path

## Working Assumption

The repository should continue to optimize for:

- correctness over cleverness
- explicit contracts over convenience
- a small, dependable public API
- strong SI behavior without sacrificing ease of custom unit-system definition
