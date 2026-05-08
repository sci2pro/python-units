# -*- coding: utf-8 -*-
"""Compatibility exports for unit definitions."""

from __future__ import annotations

import sys
from types import ModuleType

from core.quantity import unit as _extract_unit
from core.unit_definitions import (
    BaseUnit,
    CustomUnitBase,
    DerivedUnit,
    SIUnit,
    clone_unit,
    register_canonical_unit,
    require_unit_instance,
    resolve_unit,
)

__all__ = [
    "BaseUnit",
    "CustomUnitBase",
    "DerivedUnit",
    "SIUnit",
    "clone_unit",
    "register_canonical_unit",
    "require_unit_instance",
    "resolve_unit",
]


class _CallableUnitModule(ModuleType):
    """Module wrapper that preserves the public ``units.unit(...)`` helper."""

    def __call__(self, quantity: object) -> BaseUnit:
        return _extract_unit(quantity)


sys.modules[__name__].__class__ = _CallableUnitModule
