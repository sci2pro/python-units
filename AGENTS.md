# AGENTS.md

## Purpose
This repository implements a pure Python API. All contributions must prioritize:
- correctness and determinism
- clarity of interfaces
- testability and reproducibility
- minimal and explicit dependencies

---

## Core Principles

1. **Explicit is Mandatory**
   - No implicit behavior
   - No hidden side effects
   - All inputs and outputs must be well-defined

2. **Deterministic Execution**
   - No reliance on global state
   - No time-dependent logic unless explicitly required
   - Functions should be pure where possible

3. **Separation of Concerns**
   - API layer (I/O, routing) must not contain business logic
   - Business logic must not depend on frameworks
   - Data access must be isolated

4. **Fail Fast**
   - Validate inputs early
   - Raise explicit, typed exceptions
   - Do not silently coerce invalid data

---

## Required Project Structure

```
/src
  /api          # entrypoints (HTTP/CLI bindings if any)
  /core         # business logic
  /models       # data structures and schemas
  /services     # orchestration and workflows
  /adapters     # external integrations (DB, APIs, files)
  /utils        # small reusable helpers (no business logic)
/tests
  /unit
  /integration
pyproject.toml
README.md
```

### Rules
- `/core` must not import from `/api`
- `/models` must be dependency-light and reusable
- `/adapters` must be replaceable without affecting core logic

---

## API Design Rules

- All public interfaces must be:
  - typed (use type hints everywhere)
  - documented (docstrings required)

- Prefer:
  - explicit function signatures over `**kwargs`
  - immutable inputs where possible

- Avoid:
  - deeply nested data structures without schemas
  - ambiguous return types

---

## Typing

- Use standard typing (`typing`, `typing_extensions`)
- Enforce:
  - no untyped public functions
  - no `Any` unless justified

- Prefer:
  - `TypedDict`, `dataclass`, or `pydantic` models (if used)
  - clear input/output contracts

---

## Error Handling

- Define custom exception types in `/core/errors.py`
- Do not raise generic exceptions (`Exception`, `ValueError`) in core logic
- All errors must:
  - carry meaningful context
  - be actionable

Example:

```python
class InvalidInputError(Exception):
    """Raised when input data fails validation."""
```

---

## State Management

- No mutable global state
- Shared state must be:
  - passed explicitly, or
  - managed via well-defined services

- Avoid:
  - hidden caches
  - implicit singletons

---

## Dependency Management

- Dependencies must be:
  - minimal
  - justified

- Avoid:
  - heavy frameworks unless necessary
  - overlapping libraries solving the same problem

- All dependencies must be declared in `pyproject.toml`

---

## Logging

- Use structured logging
- No `print` statements in production code

Format:
```
[module] action=... status=... details=...
```

- Logging must not leak sensitive data

---

## Testing Requirements

- Every feature must include:
  - unit tests (core logic)
  - integration tests (API boundaries)

- Tests must be:
  - deterministic
  - isolated (no shared state)

- Use:
  - `pytest`

- Minimum expectations:
  - critical paths fully covered
  - edge cases explicitly tested

---

## Performance Constraints

- Avoid premature optimization
- However:
  - no unnecessary O(n²) operations
  - no repeated expensive computations without explicit caching

- Large data handling must be:
  - streaming or batched where applicable

---

## Documentation

- Every public function/class must have:
  - purpose
  - inputs
  - outputs
  - failure modes

Example:

```python
def compute_score(data: InputModel) -> Score:
    """
    Compute score from validated input data.

    Args:
        data: Structured input data.

    Returns:
        Score object.

    Raises:
        InvalidInputError: If validation fails.
    """
```

---

## Code Style

- Follow:
  - PEP 8
  - PEP 484 (typing)

- Constraints:
  - functions ≤ 50 lines unless justified
  - no deeply nested logic (>3 levels)

- Prefer:
  - small composable functions
  - explicit naming

---

## Anti-Patterns (Do Not Introduce)

- Business logic inside API handlers
- Hidden coupling between modules
- Implicit data transformations
- Overuse of decorators obscuring flow
- Catch-all exception handling
- Dynamic typing where static typing is feasible

---

## External Interfaces

- All integrations (DB, APIs, files) must:
  - live in `/adapters`
  - be abstracted behind interfaces

- Core logic must remain testable without external systems

---

## When Implementing Features

Always:
1. Define input/output contracts
2. Place logic in `/core` or `/services`
3. Isolate side effects in `/adapters`
4. Add tests before or alongside implementation
5. Validate performance implications

---

## For Complex Tasks

- Generate a step-by-step plan before coding
- Decompose into:
  - data model changes
  - core logic
  - integration points
- Implement incrementally with tests

---

## Definition of Done

A change is complete only if:
- Interfaces are typed and documented
- No hidden state or side effects exist
- Tests cover normal and edge cases
- Dependencies remain minimal
- Code is understandable without external explanation

---

## Enforcement

If any of the above rules are violated, the implementation is considered incorrect and must be revised.