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

- adopt `pyproject.toml`
- move code into `src`
- separate tests into unit and integration directories
- define a clean public API surface

### Phase 3: Interface clarity

- add full typing to public interfaces
- expand docstrings with purpose, inputs, outputs, and failure modes
- normalize naming and document compatibility aliases where needed

### Phase 4: Policy alignment

- remove or isolate Python 2 legacy behavior based on supported-version policy
- clean development dependencies and CI expectations
- ensure repository layout and tooling match `AGENTS.md`

## Immediate Recommended Next Steps

1. Freeze the intended public API and supported Python versions.
2. Add a typed error module and replace all `assert`-based validation.
3. Refactor arithmetic methods so every invalid path raises an explicit exception.
4. Move tests to deterministic `pytest` coverage with stronger edge-case coverage.
5. Migrate packaging to `pyproject.toml` and separate dev dependencies from runtime.
6. Reorganize the package into the required layered structure once behavior is locked down by tests.

## Overall Aims
- Write implementation and comprehensive unit tests. List test scenarios before writing tests.
- Cover edge cases, invalid inputs, and boundary conditions.
- Ensure 100% test coverage at all times.

## Review Notes

The library is small enough that remediation is straightforward if done in the right order: behavior first, structure second, polish third.

The strongest positive trait of the current code is conceptual simplicity. The strongest risk is that several untested operator paths and validation shortcuts could produce inconsistent behavior once the library is used beyond the narrow happy paths covered today.
