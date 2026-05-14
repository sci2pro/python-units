"""Edge-case tests for quantity, unit, and dimension contracts."""

import pytest

from core.quantity import Quantity, format_scalar, normalize_result_unit, normalize_scalar
from core.unit_definitions import BaseUnit, CustomUnitBase, DerivedUnit, clone_unit
from models.dimension import Dimension, DimensionSystem
from units import metre, second
from units.errors import InvalidUnitError, InvalidValueError, UnitOperandError


class ConstructorLimitedUnit(BaseUnit):
    """Unit subclass that exercises fallback cloning paths."""

    def __init__(self, dimension: Dimension | None = None) -> None:
        super().__init__(dimension=dimension)


def test_constructor_limited_units_preserve_state_through_fallbacks() -> None:
    source = ConstructorLimitedUnit(dimension=metre.dimension)
    source._conversion_factor = 2.0
    source._supports_multiplicative_conversion = False

    cloned = clone_unit(source)
    normalized = normalize_result_unit(source)

    assert isinstance(cloned, ConstructorLimitedUnit)
    assert cloned.dimension == metre.dimension
    assert cloned.conversion_factor == 2.0
    assert not cloned.supports_multiplicative_conversion
    assert isinstance(normalized, ConstructorLimitedUnit)
    assert normalized.dimension == metre.dimension
    assert normalized.conversion_factor == 1.0
    assert not normalized.supports_multiplicative_conversion


def test_constructor_limited_scaled_unit_builds_quantity_in_base_magnitude() -> None:
    scaled = ConstructorLimitedUnit(dimension=metre.dimension)
    scaled._conversion_factor = 1000.0

    quantity = 3 * scaled

    assert isinstance(quantity, Quantity)
    assert str(quantity) == "3000 m"


def test_quantity_reverse_quantity_operators_use_right_operand_methods() -> None:
    left = Quantity(9, metre)
    right = Quantity(4, metre)

    assert str(right.__rsub__(left)) == "5 m"
    assert str(right.__rtruediv__(left)) == "2.25"
    assert str(right.__rfloordiv__(left)) == "2"
    assert str(right.__rmod__(left)) == "1 m"
    quotient, remainder = right.__rdivmod__(left)
    assert str(quotient) == "2"
    assert str(remainder) == "1 m"


def test_quantity_scalar_operator_edges() -> None:
    distance = Quantity(9, metre)

    assert str(3 * distance) == "27 m"
    assert str(distance // 4) == "2 m"
    assert str(distance % 4) == "1 m"
    quotient, remainder = divmod(20, distance)
    assert str(quotient) == "2 m^-1"
    assert str(remainder) == "2 m^-1"

    with pytest.raises(UnitOperandError):
        distance ** complex(2, 0)


def test_unit_property_setters_and_comparisons_are_explicit() -> None:
    unit = BaseUnit()
    unit.unit_dict = {"m": 1, "s": -1}
    assert str(unit) == "m·s^-1"

    unit.dimension = second.dimension
    assert str(unit) == "s"
    assert unit != object()
    assert metre != BaseUnit(dimension=metre.dimension, conversion_factor=2.0)
    assert BaseUnit(dimension=metre.dimension, display_name="x") != BaseUnit(
        dimension=metre.dimension,
        display_name="y",
    )


def test_anonymous_display_names_are_preserved_for_explicit_units() -> None:
    named = BaseUnit(
        dimension=metre.dimension,
        conversion_factor=2.0,
        display_name="length",
    )
    dimensionless = BaseUnit()

    assert str(named) == "length"
    assert str(named / dimensionless) == "length"
    assert str((named * second) ** 1) == "length·s"
    assert str(BaseUnit(conversion_factor=2.0) ** 2) == ""
    assert BaseUnit(display_name="length").display_name == "length"
    assert (BaseUnit(display_name="length", conversion_factor=2.0) ** 2).display_name is None
    assert (named * second).display_name is None
    assert normalize_scalar(complex(1, 2)) == complex(1, 2)
    assert format_scalar(29.9999999999999) == "30"
    assert (BaseUnit(conversion_factor=2.0) / BaseUnit(conversion_factor=3.0)).display_exponents is None

    with pytest.raises(InvalidValueError):
        BaseUnit(display_exponents={1: 1})
    with pytest.raises(InvalidValueError):
        BaseUnit(display_exponents={"x": 1.5})


def test_direct_affine_base_unit_scalar_construction_preserves_metadata() -> None:
    affine = BaseUnit(
        dimension=metre.dimension,
        conversion_factor=2.0,
        conversion_offset=1.0,
        display_name="affine-length",
        supports_multiplicative_conversion=False,
    )

    quantity = 3 * affine

    assert quantity.value == 3
    assert quantity.unit.conversion_factor == 2.0
    assert quantity.unit.conversion_offset == 1.0
    assert quantity.unit.display_name == "affine-length"
    assert not quantity.unit.supports_multiplicative_conversion
    assert str(quantity) == "3 affine-length"


def test_unit_invalid_operand_edges() -> None:
    with pytest.raises(UnitOperandError):
        metre * object()
    with pytest.raises(UnitOperandError):
        object() * metre
    with pytest.raises(UnitOperandError):
        metre / object()


def test_custom_unit_definition_and_power_edges() -> None:
    class PacketUnit(CustomUnitBase):
        dimension_system = DimensionSystem("packet", ("pkt", "s"))

    packet = PacketUnit.define("pkt")
    packet_area = packet**2

    assert isinstance(packet_area, PacketUnit)
    assert str(packet_area) == "pkt^2"

    with pytest.raises(InvalidUnitError):
        PacketUnit.define("byte")
    with pytest.raises(InvalidValueError):
        PacketUnit.define("pkt", True)


def test_custom_quantity_full_units_uses_custom_rendering() -> None:
    class PacketUnit(CustomUnitBase):
        dimension_system = DimensionSystem("packet", ("pkt",))

    packet = PacketUnit.define("pkt")

    assert Quantity(5, packet).full_units == "5 pkt"


def test_unnamed_derived_unit_renders_full_units() -> None:
    unnamed = DerivedUnit(dimension=(metre / second).dimension)

    assert str(unnamed) == "m·s^-1"
    assert unnamed.full_units == "m·s^-1"


def test_dimension_rejects_bad_shapes_and_cross_system_arithmetic() -> None:
    metric_length = Dimension.from_mapping({"m": 1})
    custom_system = DimensionSystem("custom", ("x",))
    custom_length = Dimension.from_mapping({"x": 1}, system=custom_system)

    with pytest.raises(ValueError):
        Dimension(exponents=(1,))
    with pytest.raises(ValueError):
        metric_length * custom_length
    with pytest.raises(ValueError):
        metric_length / custom_length


def test_legacy_quantity_module_exports_expected_names() -> None:
    import units.quantity as quantity_module

    assert quantity_module.Quantity is Quantity
    assert quantity_module.int_quantity(Quantity(4.8, metre)).value == 4
    assert "require_quantity_operand" in quantity_module.__all__
