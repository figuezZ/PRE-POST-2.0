"""Conversiones de unidades en las fronteras de PRE-POST.

El nucleo conserva m, N y Pa. Las conversiones USCS usan las definiciones
exactas del pie (0.3048 m), la pulgada (0.0254 m), la libra internacional
(0.45359237 kg) y la gravedad estandar (9.80665 m/s2), coherentes con NIST
Special Publication 811.
"""

from dataclasses import dataclass
from enum import Enum
from math import isfinite


INCH_M = 0.0254
FOOT_M = 0.3048
POUND_MASS_KG = 0.45359237
STANDARD_GRAVITY_M_S2 = 9.80665
LBF_N = POUND_MASS_KG * STANDARD_GRAVITY_M_S2
KIP_N = 1000.0 * LBF_N
PSI_PA = LBF_N / INCH_M**2


class UnitSystem(str, Enum):
    """Sistemas disponibles en la interfaz y los reportes."""

    SI = "SI"
    USCS = "USCS"


class Quantity(str, Enum):
    """Magnitudes que requieren una unidad visible."""

    SPAN = "span"
    SECTION_LENGTH = "section_length"
    UNIT_WEIGHT = "unit_weight"
    STRESS = "stress"
    LINE_LOAD = "line_load"
    FORCE = "force"
    STEEL_AREA = "steel_area"
    SECTION_AREA = "section_area"
    INERTIA = "inertia"
    SECTION_MODULUS = "section_modulus"
    MOMENT = "moment"


@dataclass(frozen=True, slots=True)
class DisplayUnit:
    """Unidad visible y factor para convertirla a la unidad SI del nucleo."""

    symbol: str
    si_per_display_unit: float
    decimals: int


_UNITS: dict[UnitSystem, dict[Quantity, DisplayUnit]] = {
    UnitSystem.SI: {
        Quantity.SPAN: DisplayUnit("m", 1.0, 3),
        Quantity.SECTION_LENGTH: DisplayUnit("m", 1.0, 4),
        Quantity.UNIT_WEIGHT: DisplayUnit("kN/m3", 1e3, 3),
        Quantity.STRESS: DisplayUnit("MPa", 1e6, 3),
        Quantity.LINE_LOAD: DisplayUnit("kN/m", 1e3, 3),
        Quantity.FORCE: DisplayUnit("kN", 1e3, 3),
        Quantity.STEEL_AREA: DisplayUnit("mm2", 1e-6, 3),
        Quantity.SECTION_AREA: DisplayUnit("m2", 1.0, 6),
        Quantity.INERTIA: DisplayUnit("m4", 1.0, 6),
        Quantity.SECTION_MODULUS: DisplayUnit("m3", 1.0, 6),
        Quantity.MOMENT: DisplayUnit("kN m", 1e3, 3),
    },
    UnitSystem.USCS: {
        Quantity.SPAN: DisplayUnit("ft", FOOT_M, 3),
        Quantity.SECTION_LENGTH: DisplayUnit("in", INCH_M, 3),
        Quantity.UNIT_WEIGHT: DisplayUnit("pcf", LBF_N / FOOT_M**3, 3),
        Quantity.STRESS: DisplayUnit("psi", PSI_PA, 2),
        Quantity.LINE_LOAD: DisplayUnit("kip/ft", KIP_N / FOOT_M, 4),
        Quantity.FORCE: DisplayUnit("kip", KIP_N, 3),
        Quantity.STEEL_AREA: DisplayUnit("in2", INCH_M**2, 4),
        Quantity.SECTION_AREA: DisplayUnit("in2", INCH_M**2, 3),
        Quantity.INERTIA: DisplayUnit("in4", INCH_M**4, 3),
        Quantity.SECTION_MODULUS: DisplayUnit("in3", INCH_M**3, 3),
        Quantity.MOMENT: DisplayUnit("kip ft", KIP_N * FOOT_M, 3),
    },
}


def normalize_unit_system(value: UnitSystem | str) -> UnitSystem:
    """Convierte texto de interfaz en un sistema validado."""

    try:
        return value if isinstance(value, UnitSystem) else UnitSystem(value)
    except ValueError as exc:
        raise ValueError("unit_system debe ser 'SI' o 'USCS'") from exc


def display_unit(
    unit_system: UnitSystem | str, quantity: Quantity
) -> DisplayUnit:
    """Entrega simbolo, factor y precision recomendada."""

    system = normalize_unit_system(unit_system)
    return _UNITS[system][quantity]


def to_si(
    value: float, quantity: Quantity, unit_system: UnitSystem | str
) -> float:
    """Convierte un valor visible a la unidad SI utilizada por el nucleo."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("value debe ser numerico")
    if not isfinite(value):
        raise ValueError("value debe ser finito")
    return float(value) * display_unit(unit_system, quantity).si_per_display_unit


def from_si(
    value: float, quantity: Quantity, unit_system: UnitSystem | str
) -> float:
    """Convierte una magnitud SI del nucleo a la unidad visible elegida."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("value debe ser numerico")
    if not isfinite(value):
        raise ValueError("value debe ser finito")
    return float(value) / display_unit(unit_system, quantity).si_per_display_unit
