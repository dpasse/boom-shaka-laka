import numpy as np
from ..models.unit import Unit
from typing import Tuple, Dict


class UnitGenerator(object):

    def __init__(self, unit_lookup: Dict[int, Unit]):
        self.unit_lookup = unit_lookup

        super().__init__()

    def get_unit(self) -> Tuple[str, float]:
        n_units = len(self.unit_lookup.keys())
        unit = self.unit_lookup[np.random.randint(0, n_units)]

        min_value = unit.min_value
        max_value = unit.max_value

        value = np.random.randint(min_value, max_value)
        value += np.random.rand()

        value = np.around(value, 2)
        return (unit.label, value)
