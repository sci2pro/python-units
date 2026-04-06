# Contributing

## Supported Python policy

- Python 3.10 and newer are supported.
- Python 2 is not supported.
- New changes should not introduce Python 2 compatibility shims.

## Development expectations

- Prefer the public API: `from units import Quantity` and `from units.si import ...`
- Keep the `Unit` alias working until a deliberate breaking release removes it.
- Treat `long_quantity` and `long_unit` as legacy compatibility names only.
- Preserve deterministic behavior and explicit exceptions.

## Local verification

Recommended checks:

- `python3 -m pip install -e .[dev]`
- `PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_*.py'`
- `python3 -m pytest tests/unit/test_units.py`
- `python3 -m build --no-isolation --outdir artifacts/dist`
- `python3 -m twine check artifacts/dist/python_units-0.2.0.tar.gz artifacts/dist/python_units-0.2.0-py3-none-any.whl`

## Packaging and CI

- Packaging metadata lives in `pyproject.toml`.
- `setup.py` is only a setuptools compatibility shim.
- CI and publishing workflows live in `.github/workflows/`.
- Runtime business logic is layered under `src/api`, `src/core`, `src/models`, and `src/utils`.
- The public compatibility facade lives under `src/units`.
- Tests live under `tests/unit` and `tests/integration`.
