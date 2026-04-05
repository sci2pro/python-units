# -*- coding: utf-8 -*-
"""Immutable dimensional signatures for unit algebra."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping


@dataclass(frozen=True)
class Dimension:
    """Canonical exponent tuple for SI base dimensions."""

    symbols: ClassVar[tuple[str, ...]] = ('A', 'cd', 'K', 'kg', 'm', 'mol', 's')
    exponents: tuple[int, ...] = (0, 0, 0, 0, 0, 0, 0)

    def __post_init__(self) -> None:
        if len(self.exponents) != len(self.symbols):
            raise ValueError('dimension must define {} exponents'.format(len(self.symbols)))

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, int]) -> Dimension:
        """Construct a dimension from a base-symbol mapping."""
        return cls(tuple(int(mapping.get(symbol, 0)) for symbol in cls.symbols))

    def to_mapping(self) -> dict[str, int]:
        """Return a base-symbol mapping for compatibility with legacy code."""
        return dict(zip(self.symbols, self.exponents))

    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(tuple(a + b for a, b in zip(self.exponents, other.exponents)))

    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(tuple(a - b for a, b in zip(self.exponents, other.exponents)))

    def render(self) -> str:
        """Render the dimension as a unit exponent string."""
        unit_string: list[str] = []
        for key, value in zip(self.symbols, self.exponents):
            if value == 0:
                continue
            if value == 1:
                unit_string.insert(0, key)
            elif value < 0:
                unit_string.append(key + '^' + str(value))
            else:
                unit_string.insert(0, key + '^' + str(value))
        return '·'.join(unit_string)
