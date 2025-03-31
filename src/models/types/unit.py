from dataclasses import dataclass
from typing import Annotated

from pydantic import AfterValidator

_VALID_UNITS: set["_unit"] = set()


@dataclass(frozen=True)
class _unit:
    name: str
    normalized_name: str

    def __post_init__(self) -> None:
        global _VALID_UNITS
        _VALID_UNITS.add(self)

    def __hash__(self) -> int:
        return hash(self.normalized_name)


g = _unit("g", "g")
Kg = _unit("Kg", "kg")
L = _unit("L", "l")
ml = _unit("ml", "ml")
uni = _unit("uni.", "uni")
no_unit = _unit("", "")


def normalize_unit(u: str) -> str:
    return u.lower().strip(".").strip()


def validate_unit(v: str) -> str:
    if not isinstance(v, str):
        raise TypeError(f"{v!r} should be a str")

    valid_normalized_units = list(map(lambda u: u.normalized_name, _VALID_UNITS))
    if (normalized_v := normalize_unit(v)) not in valid_normalized_units:
        valid_units = list(map(lambda u: u.name, _VALID_UNITS))
        raise ValueError(f"{v!r} should be one of {', '.join(valid_units)}")

    return normalized_v


Unit = Annotated[str, AfterValidator(validate_unit)]
"""Valid ingredient unit"""
