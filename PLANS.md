# PLANS.md

## Observed Purpose

This repository currently implements a small pure-Python library for attaching units to numeric values and performing arithmetic while preserving or combining unit dimensions.

The public API is centered on:

- `BaseUnit`: stores SI dimension exponents in a dictionary
- `SIUnit`: defines named SI base units
- `DerivedUnit`: defines display names for units derived from SI dimensions
- `Unit`: pairs a numeric value with a unit and overloads arithmetic

The intended usage is:

- create values such as `Unit(3, metre)` or `Unit(5, newton)`
- enforce unit compatibility for addition and subtraction
- combine units during multiplication and division
- expose human-readable rendering for both named derived units and their SI decomposition
- allow creation of custom unit systems by subclassing `BaseUnit`

In practice, this is a compact operator-overloading utility library, not yet a structured API package in the layout required by `AGENTS.md`.

## Current Architecture

The current implementation is concentrated in a single module:

- `units/__init__.py`: all production classes, predefined units, helper functions, and a demo `main()`
- `units/tests.py`: one `unittest` module covering basic behavior
- `setup.py`: packaging metadata
- `tox.ini`: matrix for multiple Python versions

Key characteristics observed:

- business logic, data definitions, exported constants, and demo code are all colocated
- the package exports a flat API via `import units as u`
- there are no type hints on public interfaces
- most behavior is deterministic and free of external side effects
- compatibility decisions still reflect Python 2 support

## Main Gaps

### 1. Repository structure does not match project standards

Observed gap:

- the codebase does not use `/src`, `/core`, `/models`, `/services`, `/adapters`, or `/tests`
- all implementation is in `units/__init__.py`
- tests are not separated into unit and integration layers

Impact:

- weak separation of concerns
- hard to evolve without growing a god-module
- difficult to enforce clean public and internal boundaries

Required mitigation:

- migrate production code into a `src` layout
- extract core unit algebra into `src/core`
- place data structures into `src/models`
- move public exports or API bindings into `src/api` if needed
- create `tests/unit` and `tests/integration`

### 2. Public interfaces are untyped

Observed gap:

- public classes and functions have no type hints
- accepted numeric and unit inputs are implicit rather than contract-driven

Impact:

- weak editor and static-analysis support
- harder to reason about valid inputs and outputs
- increased risk of accidental misuse during refactoring

Required mitigation:

- add full type hints to public constructors, properties, and helper functions
- define explicit numeric aliases or protocols for supported scalar types
- document return types and exception behavior for every public entry point

### 3. Validation relies on `assert`

Observed gap:

- constructors and factory methods use `assert` for runtime validation
- invalid input handling is inconsistent with the repository requirement for explicit typed exceptions

Impact:

- `assert` can be disabled with optimized execution
- failures are less actionable than domain-specific exceptions
- library behavior is not robust enough for external consumers

Required mitigation:

- replace `assert` checks with explicit validation
- define domain exceptions in a dedicated error module
- ensure all invalid states raise stable, descriptive exceptions with context

### 4. Error taxonomy is incomplete and not aligned with standards

Observed gap:

- `UnitsError` and `UnitOperandError` exist, but error definitions are still embedded in the main module
- several paths fall back to Python built-in errors or implicit `None` returns

Impact:

- inconsistent failure modes
- weak consumer ergonomics
- difficult to test exhaustively

Required mitigation:

- centralize exceptions in a dedicated module such as `core/errors.py`
- ensure every unsupported operation raises a deliberate typed exception
- standardize operand and compatibility errors across all arithmetic methods

### 5. Several operator implementations are fragile

Observed gap:

- reverse subtraction delegates to `self.__sub__(unit2)`, which is semantically incorrect for `scalar - unit` or reversed unit operations
- some arithmetic methods have commented-out error branches and may return `None` for unsupported operands
- scalar checks include legacy branches such as `isinstance(unit2, oct)` and `isinstance(unit2, hex)`, which are not valid numeric type checks
- `unit` property setter uses `isinstance(unit, unit)`, which is logically incorrect

Impact:

- latent correctness bugs outside the covered test paths
- inconsistent behavior under unsupported or reversed operations
- unnecessary legacy complexity

Required mitigation:

- review every arithmetic dunder for algebraic correctness
- make unsupported operations fail explicitly rather than falling through
- remove invalid scalar type checks
- correct the unit setter implementation and add tests covering it

### 6. Test suite is narrow and partially non-deterministic

Observed gap:

- tests use `random` values without seeding even though assertions are deterministic for the generated values
- there is only one test module
- edge cases and failure cases are under-covered
- current validation used `unittest`; `pytest` is declared but was not installed in the active interpreter during review

Impact:

- limited regression protection
- poor coverage of failure modes and API boundaries
- environment drift between declared tooling and actual runnable setup

Required mitigation:

- rewrite tests into `pytest`
- remove randomness and use fixed representative values
- add coverage for invalid operands, mismatched units, reverse operators, unitless values, derived unit expansion, and string formatting edge cases
- add integration tests for packaging and import behavior

### 7. Packaging is dated and dependency metadata is noisy

Observed gap:

- packaging is driven by `setup.py`
- repository standard expects `pyproject.toml`
- `requirements.txt` contains many development and publishing packages unrelated to the runtime library
- `requirements.txt` includes an editable VCS reference to this same project

Impact:

- harder dependency auditing
- unclear separation between runtime and development dependencies
- more friction for reproducible builds

Required mitigation:

- migrate packaging metadata to `pyproject.toml`
- separate runtime dependencies from dev/test/publish dependencies
- remove self-referential editable dependency entries
- define one canonical installation path for contributors and CI

### 8. Documentation is incomplete relative to the standards

Observed gap:

- many public interfaces have minimal or outdated docstrings
- README explains basic usage but not failure modes, supported numeric semantics, or compatibility guarantees
- spelling and naming inconsistencies exist, for example `degree_celcius`

Impact:

- unclear API contract
- lower confidence for users adopting the library
- harder maintenance and future redesign

Required mitigation:

- add standard docstrings to all public classes and functions
- document inputs, outputs, and raised exceptions
- correct naming inconsistencies with a compatibility strategy if public names are already published
- update README to reflect the supported Python versions and actual package guarantees

### 9. Legacy compatibility concerns are embedded in core code

Observed gap:

- code still includes Python 2 compatibility paths such as `long`, `__div__`, and Python 2 classifiers
- the implementation mixes compatibility shims with core logic

Impact:

- more branching and lower clarity
- maintenance cost for behavior that may no longer be required
- harder modernization and typing adoption

Required mitigation:

- decide the supported Python version policy
- if Python 2 is no longer required, remove compatibility branches and simplify the implementation
- if older support must remain, isolate compatibility logic and test it intentionally

### 10. Production code contains demo behavior

Observed gap:

- `main()` in the package module prints demonstration output directly
- this mixes library code with executable sample behavior

Impact:

- blurs module responsibilities
- conflicts with the repository guidance against print-based production behavior

Required mitigation:

- move demonstrations into README examples or a dedicated example script
- keep package modules focused on reusable library behavior only

## Prioritized Mitigation Plan

### Phase 1: Correctness and contract hardening

- replace `assert` validation with explicit exceptions
- fix incorrect operator implementations and unsupported operand handling
- add deterministic tests for all public arithmetic and failure paths
- define and centralize domain exception types

### Phase 2: Packaging and structure modernization

- introduce the new public API without breaking existing users
- add `Quantity` as the preferred value type and keep `Unit` as a compatibility alias
- add `units.si` as the canonical location for predefined units
- keep top-level unit re-exports during the compatibility window
- reorganize implementation into focused modules so the public API is curated rather than incidental
- adopt `pyproject.toml`
- move code into `src`
- separate tests into unit and integration directories
- test both legacy and new import paths during the transition

### Phase 3: CI/CD and publish automation

- add GitHub Actions workflows modeled after the approach used in `sci2pro/wowdata`
- run CI on push and pull request
- test the supported Python version matrix
- build and verify source and wheel distributions
- run the project test suite from the canonical install path
- add release automation for publishing to TestPyPI and/or PyPI
- restrict publish jobs to tagged releases or explicit release events
- document required repository secrets and release steps
- add status badges and contributor guidance for the new workflows

Reason for this placement:

- the new API and package layout need to exist first so CI reflects the intended installation and import paths
- automation should be in place before later deprecations and breaking-release work so transition releases are reproducible and safe

### Phase 4: Interface clarity

- complete the public API redesign around `Quantity` plus `units.si`
- add full typing to public interfaces
- expand docstrings with purpose, inputs, outputs, and failure modes
- normalize naming and document compatibility aliases where needed
- publish a migration guide from `import units as u` to the new import style
- make deprecation policy explicit in documentation and release notes
- define the stable top-level exports and stop leaking internal structure accidentally

### Phase 5: Policy alignment

- decide and document the supported Python version policy
- remove or isolate Python 2 legacy behavior based on that policy
- clean development dependencies and CI expectations
- ensure repository layout and tooling match `AGENTS.md`
- define which semantic constraints belong in the core package and which belong in higher-level domain types
- keep the core quantity model signed and dimensionally correct while reserving non-negativity rules for constrained domain types
- decide whether constrained concepts such as `Length`, `Distance`, or `Duration` belong in this package or in a later layer built on top of it

### Phase 6: Breaking-change release readiness

- maintain backward compatibility until the new API is stable and documented
- verify that both old and new APIs are covered by tests throughout the transition period
- audit warnings so they are informative without becoming noisy
- remove deprecated aliases only in a deliberate breaking release
- target removal of legacy paths no earlier than a major release boundary such as `1.0.0`
- ensure release notes include a concise migration table and examples

### Phase 7: New features

- include imperial units
- convert between metric and imperial units

## Immediate Recommended Next Steps

1. Freeze the intended public API and supported Python versions.
2. Add a typed error module and replace all `assert`-based validation.
3. Refactor arithmetic methods so every invalid path raises an explicit exception.
4. Move tests to deterministic `pytest` coverage with stronger edge-case coverage.
5. Migrate packaging to `pyproject.toml` and separate dev dependencies from runtime.
6. Introduce `Quantity` and `units.si` additively before removing any legacy API paths.
7. Add CI/CD and publish workflows once the new install and import paths are defined.
8. Reorganize the package into the required layered structure once behavior is locked down by tests and the compatibility story is defined.

## Overall Aims
- Write implementation and comprehensive unit tests. List test scenarios before writing tests.
- Cover edge cases, invalid inputs, and boundary conditions.
- Ensure 100% test coverage at all times.

## Review Notes

The library is small enough that remediation is straightforward if done in the right order: behavior first, structure second, polish third.

The strongest positive trait of the current code is conceptual simplicity. The strongest risk is that several untested operator paths and validation shortcuts could produce inconsistent behavior once the library is used beyond the narrow happy paths covered today.

## Package Coherence Assessment

### Is this a coherent package?

Yes at the concept level, not yet at the package-design level.

The codebase has a clear single responsibility:

- represent quantities with units
- preserve dimensions through arithmetic
- reject invalid operations when units are incompatible

That makes the domain model coherent.

The package is not yet coherent as a maintained public API because:

- unit definitions, quantity behavior, helper conversions, exported constants, and demo code are mixed in one module
- internal and public concepts are not clearly separated
- the naming is misleading: the current `Unit` type is really a quantity/value object, while `BaseUnit`, `SIUnit`, and `DerivedUnit` are the actual unit definitions
- there is no explicit boundary between stable public API and internal implementation detail

Conclusion:

- coherent purpose: yes
- coherent domain model: mostly yes
- coherent package/interface design: no, not in its current form

## Recommended Public API

### Design goals

The public API should be:

- small
- explicit
- typed
- stable
- unsurprising to users who already understand physical quantities

The API should distinguish clearly between:

- a unit definition
- a measured quantity using that unit

### Recommended core concepts

The recommended public surface should center on four concepts:

- `Quantity`: a numeric value coupled to a unit
- `Unit`: an immutable unit definition
- predefined unit constants, for example `metre`, `second`, `newton`
- domain exceptions, imported from a dedicated errors module

Optional internal concept:

- `Dimension`: the exponent map behind a unit; this may remain internal unless advanced users need direct access

### Recommended naming

Current naming should be normalized as follows:

- current `Unit` class should become `Quantity`
- current `BaseUnit` should become the general `Unit` abstraction
- current `SIUnit` and `DerivedUnit` should become implementation details or subclasses beneath `Unit`

Reason:

- `Quantity(3, metre)` is semantically clear
- `Unit` should mean a unit definition, not a measured value

### Recommended import style

The top-level package should expose a curated public API:

```python
from units import Quantity, Unit
from units.si import metre, second, newton
from units.errors import UnitCompatibilityError

distance = Quantity(3, metre)
time = Quantity(2, second)
speed = distance / time
```

Alternative convenience export:

```python
import units.si as u
from units import Quantity

distance = Quantity(3, u.metre)
time = Quantity(2, u.second)
```

### Recommended behavior rules

The API should define the following semantics explicitly:

- `Quantity + Quantity` and `Quantity - Quantity` require identical units
- `Quantity * Quantity` and `Quantity / Quantity` combine units algebraically
- `Quantity * scalar` and `Quantity / scalar` are allowed
- `scalar / Quantity` is allowed and returns an inverse unit quantity
- `modulo` should either require identical units or be removed if the package wants stricter physical semantics
- `floor division` should be supported only for real scalars and real-valued quantities
- unitless quantities should be explicit and first-class

### Recommended domain constraints

The package should support domain-level semantic constraints, not just dimensional correctness.

One important example is non-negativity for physical measures such as:

- length
- distance
- duration
- mass
- absolute temperature

The design should reinforce the idea that dimensional validity alone is not enough. A value can have the correct unit and still be physically invalid for a specific domain concept.

Example:

- a quantity measured in metres may be dimensionally valid
- a negative length may still be semantically invalid for many use cases
- a negative displacement or signed position in metres may still be semantically valid

Recommended mitigation:

- keep the core `Quantity` type signed and dimensionally correct by default
- support optional validation policies or constrained quantity types for domains that must be non-negative
- avoid treating unit definitions themselves as carriers of non-negativity rules
- define whether subtraction that would cross below zero should raise an error only for constrained domain types, not for the generic quantity type
- distinguish clearly between concepts such as `length` and `displacement`, since the former is commonly non-negative while the latter may legitimately be negative

This means the long-term API should not only model units; it should also leave room for quantity semantics and domain invariants.

Conclusion:

- `-30 metres` should remain representable in the core package
- whether it is admissible should depend on the semantic type being modeled, not on the unit alone

### Recommended module layout

The public package should be reorganized into focused modules:

- `units/__init__.py`: curated exports only
- `units/quantity.py`: `Quantity`
- `units/unit.py`: `Unit` definitions and algebra
- `units/si.py`: predefined SI and derived units
- `units/errors.py`: public exceptions
- `units/formatting.py`: string formatting and rendering logic if kept separate

If the broader repository migration to `src` proceeds, the equivalent layout should live under `src/units` or `src/core` with the same public boundary.

### Recommended public API contents

The stable top-level public API should likely include:

- `Quantity`
- `Unit`
- `int_quantity`, `float_quantity`, `complex_quantity` only if these helpers remain justified
- `UnitsError`
- `InvalidUnitError`
- `InvalidValueError`
- `UnitCompatibilityError`
- `UnitOperandError`

The top-level package should not expose:

- demo functions such as `main()`
- low-level mutable implementation details
- compatibility shims that only exist for legacy Python support

### Recommended migration strategy

To avoid breaking existing users immediately:

1. Introduce `Quantity` as the preferred public name.
2. Keep `Unit` as a compatibility alias for one or more releases if needed.
3. Move predefined units into a dedicated module and re-export them temporarily from the top level.
4. Deprecate helper names and legacy behavior with explicit warnings if the package is actively published.
5. Remove ambiguous names only after the public contract is documented and tests cover the migration path.

## Backward Compatibility Plan

The preferred new API is:

```python
from units import Quantity
from units.si import metre, second, newton
```

This API should be introduced without immediately removing the legacy API.

### Compatibility principle

The package should change the preferred API before it changes the supported API.

That means:

- new code should be guided to the `Quantity` plus `units.si` import style
- existing code using `import units as u` should continue to run during a transition window

### Compatibility requirements

During the transition period:

- `Unit` should remain available as a compatibility alias for `Quantity`
- top-level exports such as `metre`, `second`, and `newton` should remain re-exported
- legacy import patterns should continue to function
- deprecated entry points should emit warnings with a clear migration path

### Recommended release sequence

Suggested rollout:

- `0.1.4`
  - add `Quantity`
  - add `units.si`
  - keep `Unit` and top-level unit exports working
  - update documentation to prefer the new API
  - add deprecation warnings only where necessary and low-noise

- `0.1.5` or `0.2.0`
  - continue supporting both APIs
  - make deprecation guidance more explicit
  - ensure tests cover both the new and legacy interfaces

- `1.0.0`
  - remove deprecated aliases only if the migration guide has been published, the deprecation window has been honored, and the maintainer is ready to enforce the cleaner API

### Testing requirements for compatibility

The test suite should explicitly verify:

- the new API works as documented
- the old API still works during the transition
- `Unit is Quantity` or equivalent alias behavior is preserved where intended
- top-level unit exports match the objects from `units.si`
- deprecation warnings appear where expected and not on every normal code path

### Documentation requirements for compatibility

The README and release notes should include a minimal migration guide.

Example:

```python
# Old
import units as u
distance = u.Unit(3, u.metre)

# New
from units import Quantity
from units.si import metre
distance = Quantity(3, metre)
```

### Removal criteria

Legacy API entry points should only be removed when all of the following are true:

- the replacement API is stable
- compatibility aliases have existed for at least one transition release
- release notes have clearly announced the removal timeline
- tests and documentation no longer depend on the legacy path

## Interface Decision Summary

The right API is not a broad framework. It is a compact domain package with:

- one value object: `Quantity`
- one unit-definition abstraction: `Unit`
- one standard library of predefined units
- one explicit exception hierarchy

That keeps the conceptual model aligned with the actual purpose of the project while making the package boundary cleaner, easier to document, and easier to evolve safely.

## Dimensional Model Recommendation

### Is exponent algebra the right approach?

Yes.

Representing units as exponents over a fixed base-dimension system is the right core mathematical model for this package.

Why it works:

- multiplication corresponds to addition of exponents
- division corresponds to subtraction of exponents
- compatibility checks become equality checks on dimension signatures
- derived-unit recognition becomes possible from the resulting dimension signature

This means the current conceptual approach is sound.

### What is weak in the current representation?

The current implementation uses mutable dictionaries keyed by unit symbols.

That is acceptable as a prototype, but it is weaker than it should be for long-term API and canonicalization work because:

- dictionaries are mutable
- keys are stringly typed
- equality depends on a runtime mapping rather than a canonical dimension value object
- there is no registry that maps a computed dimension back to a preferred named unit such as `volt`
- the implementation mixes unit identity, dimension algebra, and display behavior too closely

### Recommended long-term model

The package should separate three related but distinct concepts:

1. `Dimension`
   An immutable canonical signature of exponents over the base dimensions.

2. `Unit`
   A unit definition that carries:
   - a `Dimension`
   - a symbol
   - a name
   - a scale factor
   - optionally an offset for units that need affine conversion semantics

3. `Quantity`
   A numeric value paired with a `Unit`

This design is stronger than the current dictionary-based model because it creates a stable identity for dimensions and opens the door to canonicalization and conversion logic.

### Recommended representation

The preferred internal representation for dimensions should be immutable and fixed-order, for example:

```python
Dimension(exponents=(A, cd, K, kg, m, mol, s))
```

or equivalently a tuple in a fixed SI order.

Reason:

- dimension equality becomes cheap and unambiguous
- hashing becomes straightforward
- dimensions can be used as registry keys
- canonicalization becomes much easier

### Canonicalization and named-unit resolution

If the package should resolve expressions such as:

- `watt / ampere` to `volt`
- `joule / coulomb` to `volt`
- `newton * metre` to `joule`

then it needs a registry of preferred named units keyed by canonical dimensions.

Recommended design:

- compute the resulting dimension from algebra
- normalize to a canonical `Dimension`
- look up that dimension in a registry of known units
- if a preferred named unit exists, use it for formatting or simplification
- otherwise fall back to explicit exponent rendering

Important distinction:

- dimensional equivalence is mathematical
- choice of preferred rendering is a canonicalization policy

That means `J/C` and `V` may be equivalent in dimension while the package still gets to decide whether to preserve the original expression or simplify to `V`.

### Recommended architectural direction

The package should evolve toward:

- immutable `Dimension` objects
- immutable `Unit` definitions
- registry-backed named-unit canonicalization
- `Quantity` objects that use unit and dimension metadata rather than ad hoc symbol dictionaries

### Practical payoff

This change would make the package better at:

- recognizing consolidated derived units
- supporting deterministic simplification rules
- adding unit conversion later
- separating mathematical identity from display formatting
- supporting a larger and cleaner library of named units

### Planning implication

This should be treated as a later architectural enhancement, not part of the immediate compatibility work.

The current exponent-algebra approach should be retained, but the representation should be upgraded when the package moves beyond its current transitional API phase.
