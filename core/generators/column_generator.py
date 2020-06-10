import numpy as np
from typing import Iterator, Tuple
from .label_generator import LabelGenerator
from .unit_generator import UnitGenerator
from ..models.unit import get_unit_lookup
from ..models.column import Column
from ..models.unit import Unit


class ColumnGenerator(object):

    def __init__(self, label_generator: LabelGenerator, unit_generator: UnitGenerator):
        self.label_generator = label_generator
        self.unit_generator = unit_generator

        super().__init__()

    def generate_label(self, column: Column) -> Tuple[Iterator[str], Unit]:
        min_label_width: int = column.min_label_length
        max_label_width: int = column.max_label_length
        n_labels: int = np.random.randint(1, column.max_number_of_label_parts)

        labels = self.label_generator.get_many_labels(min_label_width, max_label_width, n_labels)
        unit = self.unit_generator.get_unit()

        ## name and unit,
        return labels, unit

    def get_column(self, column: Column):
        min_label_width: int = column.min_label_length
        max_label_width: int = column.max_label_length
        n_labels: int = np.random.randint(1, column.max_number_of_label_parts)

        unit = self.unit_generator.get_unit()
        unit_value = self.unit_generator.get_value(unit)

        labels = self.label_generator.get_many_labels(min_label_width, max_label_width, n_labels)

        unit_rows = column.compress_unit(unit, unit_value)
        label_rows = column.compress_column(labels)

        labels = ' '.join(label_rows)
        units = ' '.join(unit_rows)
        target = f'{labels} {units}'
        return (column.zip(label_rows, unit_rows), target)

    def get_value_for_label(self, column: Column, labels: Iterator[str], unit: Unit):
        unit_rows = column.compress_unit(
            unit.label,
            self.unit_generator.get_value(unit)
        )

        label_rows = column.compress_column(labels)

        labels = ' '.join(label_rows)
        units = ' '.join(unit_rows)
        target = f'{labels} {units}'

        return (column.zip(label_rows, unit_rows), target)
