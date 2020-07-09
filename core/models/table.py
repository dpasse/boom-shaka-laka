import re
import uuid

from typing import List
from .column import Column


class Table(object):
    id: str
    max_number_of_labels: int ## per column
    n_spaces_between_columns: int
    columns: List[Column]

    def __init__(self):
        self.id = uuid.uuid4().hex

        super().__init__()

    def get_id(self):
        return self.id

    def set_id(self, id: str):
        self.id = id ## save / reload tables

    def get_max_size(self):
        table_height = 0
        table_width = 0

        calculated_table_width = 1 ## '\n'
        worst_possible_number_of_labels = 0
        for column in self.columns:
            calculated_table_width += (column.max_label_length + column.max_unit_length)

            if column.max_number_of_label_parts > worst_possible_number_of_labels:
                worst_possible_number_of_labels = column.max_number_of_label_parts

        calculated_table_width += ((len(self.columns) - 1) * self.n_spaces_between_columns)
        calculated_table_height = worst_possible_number_of_labels * self.max_number_of_labels

        if calculated_table_width > table_width:
            table_width = calculated_table_width

        if calculated_table_height > table_height:
            table_height = calculated_table_height

        return table_width, table_height

    def get_split_targets(self) -> List[int]:
        targets: List[int] = []
        if len(self.columns) <= 1:
            return targets

        previous_target = 0
        for column in self.columns[:-1]:
            target = column.max_label_length + column.max_unit_length + self.n_spaces_between_columns
            targets.append(
                previous_target + target
            )

            previous_target = target

        return targets

    def compress(self, column_values: List[List[str]]) -> List[str]:
        current_row_index = 0
        rows = [ ]

        r_i = 0
        while True:

            row = ''

            quit = False

            for column in self.columns:
                c_i = column.order

                val = ''
                if len(column_values[c_i]) > r_i:
                    val += column_values[c_i][r_i]
                    quit = False
                else:
                    quit = True

                padding = column.column_length() - len(val)
                val += ''.join([ ' ' for _ in range(padding)])
                val += ''.join([ ' ' for _ in range(self.n_spaces_between_columns)])
                row += val

            rows.append(re.sub(r'[ ]+$', '', row))
            r_i += 1

            if quit:
                break

        return rows
