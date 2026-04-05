"""Unit tests for quantity and unit behavior."""

import pytest

import units.si as si
from units import (
    CustomUnitBase,
    Quantity,
    SIUnit,
    Unit,
    ampere,
    becquerel,
    candela,
    coulomb,
    complex_unit,
    degree_celcius,
    farad,
    float_quantity,
    float_unit,
    gray,
    henry,
    hertz,
    int_quantity,
    int_unit,
    joule,
    katal,
    kelvin,
    kilogram,
    long_unit,
    lumen,
    lux,
    metre,
    mole,
    newton,
    ohm,
    pascal,
    radian,
    second,
    siemens,
    sievert,
    steradian,
    tesla,
    volt,
    watt,
    weber,
)
from units.dimension import DimensionSystem
from units.errors import (
    InvalidUnitError,
    InvalidValueError,
    UnitCompatibilityError,
    UnitOperandError,
)


def test_new_api_imports() -> None:
    distance = 3 * si.metre
    time = 2 * si.second
    force = 5 * si.newton

    assert str(distance) == "3 m"
    assert str(time) == "2 s"
    assert str(force) == "5 N"
    assert str(distance / time) == "1.5 m·s^-1"
    assert str(Quantity(3, si.metre)) == "3 m"


def test_legacy_api_compatibility() -> None:
    assert Unit is Quantity
    assert metre is si.metre
    assert second is si.second
    assert newton is si.newton


@pytest.mark.parametrize(
    ("unit", "expected"),
    [
        (metre, "7 m"),
        (second, "7 s"),
        (kilogram, "7 kg"),
        (kelvin, "7 K"),
        (candela, "7 cd"),
        (ampere, "7 A"),
        (mole, "7 mol"),
    ],
)
def test_si_units(unit, expected: str) -> None:
    assert str(Unit(7, unit)) == expected


@pytest.mark.parametrize(
    ("unit", "expected"),
    [
        (radian, "7 rad"),
        (steradian, "7 sr"),
        (hertz, "7 Hz"),
        (newton, "7 N"),
        (pascal, "7 Pa"),
        (joule, "7 J"),
        (watt, "7 W"),
        (coulomb, "7 C"),
        (volt, "7 V"),
        (farad, "7 F"),
        (ohm, "7 Ω"),
        (siemens, "7 S"),
        (weber, "7 Wb"),
        (tesla, "7 T"),
        (henry, "7 H"),
        (degree_celcius, "7 °C"),
        (lumen, "7 lm"),
        (lux, "7 lx"),
        (becquerel, "7 Bq"),
        (gray, "7 Gy"),
        (sievert, "7 Sv"),
        (katal, "7 kat"),
    ],
)
def test_derived_units(unit, expected: str) -> None:
    assert str(Unit(7, unit)) == expected


def test_quantity_properties() -> None:
    quantity = Unit(11, metre)
    assert quantity.value == 11
    assert str(quantity.unit) == "m"
    assert str(quantity.full_units) == "11 m"
    assert not quantity.is_unitless


def test_scalar_operations() -> None:
    quantity = Unit(12, metre)
    assert str(quantity * 4) == "48 m"
    assert str(quantity / 3) == "4.0 m"
    assert str(24 / quantity) == "2.0 m^-1"
    assert str(24 // quantity) == "2 m^-1"
    assert str(25 % quantity) == "1 m^-1"


def test_scalar_unit_construction() -> None:
    assert str(3 * metre) == "3 m"
    assert str(metre * 3) == "3 m"
    assert str(2.5 * newton) == "2.5 N"


def test_quantity_unit_algebra() -> None:
    speed = (10 * metre) / second
    area = (3 * metre) * metre
    assert str(speed) == "10 m·s^-1"
    assert str(area) == "3 m^2"


def test_power_operators() -> None:
    assert str(5 * metre**3) == "5 m^3"
    assert str((3 * metre) ** 2) == "9 m^2"
    assert str((2 * volt) ** 2) == "4 V^2"
    assert str(Quantity(4) ** 0.5) == "2.0"

    with pytest.raises(InvalidValueError):
        metre ** 1.5
    with pytest.raises(UnitOperandError):
        (3 * metre) ** 0.5


def test_invalid_operations() -> None:
    with pytest.raises(TypeError):
        complex(Unit(1.5, metre))
    with pytest.raises(TypeError):
        int(Unit(1.5, metre))
    with pytest.raises(TypeError):
        float(Unit(1.5, metre))
    with pytest.raises(UnitCompatibilityError):
        Unit(2, metre) + Unit(3, second)
    with pytest.raises(UnitCompatibilityError):
        Unit(2, metre) % Unit(3, second)
    with pytest.raises(UnitOperandError):
        Unit(2, metre) + 3
    with pytest.raises(UnitOperandError):
        3 + Unit(2, metre)
    with pytest.raises(UnitOperandError):
        Unit(2, metre) * object()
    with pytest.raises(UnitOperandError):
        Unit(2, metre) // complex(2, 1)
    with pytest.raises(InvalidValueError):
        Unit("3", metre)
    with pytest.raises(InvalidUnitError):
        Unit(3, "metre")


def test_unary_operators() -> None:
    positive = Unit(9, metre)
    negative = Unit(-9, metre)
    assert str(-positive) == "-9 m"
    assert str(-negative) == "9 m"
    assert str(+positive) == "9 m"
    assert str(+negative) == "-9 m"
    assert str(abs(positive)) == "9 m"
    assert str(abs(negative)) == "9 m"


def test_operations_between_quantities() -> None:
    x = Unit(9.0, metre)
    y = Unit(4.0, metre)
    assert str(x + y) == "13.0 m"
    assert str(y + x) == "13.0 m"
    assert str(x - y) == "5.0 m"
    assert str(y - x) == "-5.0 m"
    assert str(x * y) == "36.0 m^2"
    assert str(x / y) == "2.25"
    assert str(x // y) == "2.0"
    assert str(x % y) == "1.0 m"
    quotient, remainder = divmod(x, y)
    assert str(quotient) == "2.0"
    assert str(remainder) == "1.0 m"


def test_type_conversions() -> None:
    assert str(int_unit(Unit(4.8, metre))) == "4 m"
    assert str(float_unit(Unit(7, metre))) == "7.0 m"
    assert str(long_unit(Unit(4.8, metre))) == "4 m"
    assert str(complex_unit(Unit(4.8, metre))) == "(4.8+0j) m"
    assert str(int_quantity(Quantity(4.8, metre))) == "4 m"
    assert str(float_quantity(Quantity(7, metre))) == "7.0 m"


def test_operation_derived() -> None:
    result = Unit(6.0, newton) / Unit(2.0, radian)
    assert isinstance(str(result), str)
    assert result.full_units == "3.0 m·kg·s^-2"


def test_canonical_named_unit_resolution() -> None:
    assert str(Unit(3, watt) / Unit(1, ampere)) == "3.0 V"
    assert str(Unit(2, newton) * Unit(5, metre)) == "10 J"
    assert str(Unit(8, volt) / Unit(2, ampere)) == "4.0 Ω"


def test_ambiguous_dimensions_do_not_canonicalize() -> None:
    assert str(Unit(5, SIUnit() / second)) == "5 s^-1"
    assert str(Unit(5, joule / kilogram)) == "5 m^2·s^-2"


def test_custom_unit_systems() -> None:
    class CommUnit(CustomUnitBase):
        dimension_system = DimensionSystem("comm", ("b", "s", "B"))

    bit = CommUnit.define("b")
    second_comm = CommUnit.define("s")

    rate = Quantity(32, bit) / Quantity(4, second_comm)
    assert str(rate) == "8.0 b·s^-1"

    with pytest.raises(UnitCompatibilityError):
        Quantity(1, metre) * Quantity(1, bit)


def test_reverse_unit_operations() -> None:
    x = Unit(5, metre)
    y = Unit(14, metre)
    assert str(y - x) == "9 m"
    assert str(y / x) == "2.8"


def test_unitless_values() -> None:
    unitless = Unit(3)
    assert unitless.is_unitless
    assert str(unitless) == "3"
    assert str(unitless * Unit(2, metre)) == "6 m"
    assert str(Unit(2, metre) / unitless) == "0.6666666666666666 m"


def test_setters_and_definitions() -> None:
    quantity = Unit(3, metre)
    quantity.value = 4.5
    quantity.unit = second
    assert str(quantity) == "4.5 s"

    with pytest.raises(InvalidValueError):
        quantity.value = "invalid"
    with pytest.raises(InvalidUnitError):
        quantity.unit = "invalid"
    with pytest.raises(InvalidUnitError):
        SIUnit.define("invalid")
    with pytest.raises(InvalidValueError):
        SIUnit.define("m", 1.2)


def test_helper_rejects_invalid_operand() -> None:
    with pytest.raises(UnitOperandError):
        int_unit(3)
    with pytest.raises(UnitOperandError):
        float_unit(3)
    with pytest.raises(UnitOperandError):
        long_unit(3)
    with pytest.raises(UnitOperandError):
        complex_unit(3)
