import numpy as np
from typing import Iterator
from .column_generator import ColumnGenerator
from ..models.table import Table


class TableGenerator(object):

    def __init__(self, column_generator: ColumnGenerator):
        self.colum_generator = column_generator

        super().__init__()

    def get_table(self, table: Table):
        ## we want this to grow right,
        actual_table = [ [] for _ in table.columns ]

        ## we want this to be flat,
        target_table = []

        for column in table.columns:
            n_labels = np.random.randint(1, table.max_number_of_labels)

            for i in range(n_labels):
                actual, expected = self.colum_generator.get_column(column)

                for row in actual:
                    actual_table[column.order].append(row)

                target_table.append(expected)

        return table.compress(actual_table), '\n'.join(target_table)
