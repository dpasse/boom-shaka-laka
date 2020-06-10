import numpy as np
from typing import Iterator
from .unit import Unit


class Column(object):
    order: int

    min_label_length: int
    max_label_length: int
    max_unit_length: int
    max_number_of_label_parts: int

    def column_length(self):
        return self.max_unit_length + self.max_label_length

    def compress_column(self, labels: Iterator[str]) -> Iterator[str]:
        current_row_index = 0
        rows = [ labels[0] ]

        for index in range(1, len(labels)):
            label = labels[index]
            value = f'{rows[current_row_index]} {label}'

            if len(value) <= self.max_label_length:
                rows[current_row_index] = value
            else:
                rows.append(label)
                current_row_index += 1

        return rows

    def compress_unit(self, unit: str, unit_value: float) -> Iterator[str]:
        rows = [ str(unit_value) ]
        value = f'{rows[0]} {unit}'

        if len(value) <= self.max_unit_length:
            rows[0] = value
        else:
            rows.append(unit)

        return rows

    def zip(self, labels: Iterator[str], units: Iterator[str]) -> Iterator[str]:
        rows = []

        n_labels = len(labels)
        n_units = len(units)
        for index in range(0, np.max([n_labels, n_units])):
            row = ''

            if index < n_labels:
                row = labels[index]

            row_length = len(row)
            if row_length < self.max_label_length:
                padding = self.max_label_length - row_length
                row += ''.join([ ' ' for _ in range(0, padding)])

            if index < len(units):
                unit = units[index]
                row += unit

            rows.append(row)

        return rows
