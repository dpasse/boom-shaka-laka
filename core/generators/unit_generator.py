import numpy as np
from ..models.unit import Unit
from typing import Tuple, Dict


class UnitGenerator(object):

    def __init__(self, unit_lookup: Dict[int, Unit]):
        self.unit_lookup = unit_lookup

        super().__init__()

    def get_unit(self) -> Unit:
        n_units = len(self.unit_lookup.keys())
        return self.unit_lookup[np.random.randint(0, n_units)]

    def get_value(self, unit: Unit) -> float:
        value = np.random.randint(unit.min_value, unit.max_value)
        value += np.random.rand()
        return np.around(value, 2)
