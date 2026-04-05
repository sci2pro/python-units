"""Integration tests for public import paths."""

import api.public as public_api
import units
import units.si as units_si
from core.quantity import Quantity as CoreQuantity
from models.dimension import DimensionSystem


def test_units_facade_matches_public_api() -> None:
    assert units.Quantity is public_api.Quantity
    assert units.Unit is public_api.Unit
    assert units.metre is units_si.metre
    assert units.second is units_si.second


def test_public_quantity_construction_and_custom_units() -> None:
    class CommUnit(units.CustomUnitBase):
        dimension_system = DimensionSystem("comm", ("b", "s"))

    bit = CommUnit.define("b")
    second = CommUnit.define("s")

    rate = (32 * bit) / (4 * second)

    assert isinstance(3 * units.metre, CoreQuantity)
    assert str(rate) == "8.0 b·s^-1"
