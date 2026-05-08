# -*- coding: utf-8 -*-
"""Immutable dimensional signatures for unit algebra."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Mapping


@dataclass(frozen=True)
class DimensionSystem:
    """Ordered base-dimension system for a family of units."""

    name: str
    symbols: tuple[str, ...]


SI_DIMENSION_SYSTEM = DimensionSystem("si", ("A", "cd", "K", "kg", "m", "mol", "s"))


@dataclass(frozen=True)
class Dimension:
    """Canonical exponent tuple for a dimension system."""

    default_system: ClassVar[DimensionSystem] = SI_DIMENSION_SYSTEM
    system: DimensionSystem = SI_DIMENSION_SYSTEM
    exponents: tuple[int, ...] = (0, 0, 0, 0, 0, 0, 0)

    def __post_init__(self) -> None:
        if len(self.exponents) != len(self.system.symbols):
            raise ValueError(
                "dimension must define {} exponents".format(len(self.system.symbols))
            )
        for exponent in self.exponents:
            if not isinstance(exponent, int) or isinstance(exponent, bool):
                raise ValueError(
                    "dimension exponents must be integers, got {}".format(
                        type(exponent).__name__
                    )
                )

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, int],
        system: DimensionSystem | None = None,
    ) -> "Dimension":
        """Construct a dimension from a base-symbol mapping."""
        dimension_system = system or cls.default_system
        unknown_symbols = set(mapping) - set(dimension_system.symbols)
        if unknown_symbols:
            raise ValueError(
                "unknown dimension symbols: {}".format(", ".join(sorted(unknown_symbols)))
            )
        return cls(
            system=dimension_system,
            exponents=tuple(
                cls._validate_exponent(mapping.get(symbol, 0))
                for symbol in dimension_system.symbols
            ),
        )

    @staticmethod
    def _validate_exponent(exponent: object) -> int:
        """Return a valid exponent or raise for invalid exponent input."""
        if not isinstance(exponent, int) or isinstance(exponent, bool):
            raise ValueError(
                "dimension exponents must be integers, got {}".format(
                    type(exponent).__name__
                )
            )
        return exponent

    def to_mapping(self) -> dict[str, int]:
        """Return a base-symbol mapping for compatibility with public APIs."""
        return dict(zip(self.system.symbols, self.exponents))

    def __mul__(self, other: "Dimension") -> "Dimension":
        if self.system != other.system:
            raise ValueError("cannot combine dimensions from different systems")
        return Dimension(
            system=self.system,
            exponents=tuple(a + b for a, b in zip(self.exponents, other.exponents)),
        )

    def __truediv__(self, other: "Dimension") -> "Dimension":
        if self.system != other.system:
            raise ValueError("cannot combine dimensions from different systems")
        return Dimension(
            system=self.system,
            exponents=tuple(a - b for a, b in zip(self.exponents, other.exponents)),
        )

    def render(self) -> str:
        """Render the dimension as a unit exponent string."""
        unit_string: list[str] = []
        for key, value in zip(self.system.symbols, self.exponents):
            if value == 0:
                continue
            if value == 1:
                unit_string.insert(0, key)
            elif value < 0:
                unit_string.append(key + "^" + str(value))
            else:
                unit_string.insert(0, key + "^" + str(value))
        return "·".join(unit_string)
