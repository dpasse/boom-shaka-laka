from typing import Iterator


class Unit(object):
    label: str
    min_value: int
    max_value: int

    def __init__(self, label, min_value, max_value):
        self.label = label
        self.min_value = min_value
        self.max_value = max_value

_units = [
    Unit('m/s', 0, 3),
    Unit('cm/s', 0, 3),
    Unit('cm', 0, 5),
    Unit('m', 0, 5)
]

def get_units() -> Iterator[Unit]:
    return _units

def get_unit_lookup() -> dict:
    return dict([
        (i, u)
        for i, u
        in enumerate(_units)
    ])
