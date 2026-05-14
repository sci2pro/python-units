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


def test_public_conversion_api() -> None:
    import units.unit as unit_module

    distance = 1.5 * units.kilometre

    assert str(distance.to(units.metre)) == "1500 m"
    assert str(units.convert(2500 * units.metre, units.kilometre)) == "2.5 km"
    assert units.value(distance) == 1.5
    assert units.unit(distance) == units.kilometre
    assert unit_module(distance) == units.kilometre
    assert units.multiplier(units.kilometre) == 1000.0
    assert units.multiplier(units.picometre) == 0.000000000001
    assert units_si.kilometre is units.kilometre
    assert units_si.picosecond is units.picosecond


def test_public_imperial_namespace() -> None:
    from units.imperial import fahrenheit, foot, mile, pound

    assert str(1 * mile) == "1 mi"
    assert str((3 * foot).to(units.metre)) == "0.9144 m"
    assert str((1 * pound).to(units.gram)) == "453.59237 g"
    assert str((32 * fahrenheit).to(units.degree_celcius)) == "0 °C"
