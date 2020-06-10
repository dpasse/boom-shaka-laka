import numpy as np
from typing import Iterator, Tuple
from .column_generator import ColumnGenerator
from ..models.table import Table
from collections import defaultdict

class TableGenerator(object):

    def __init__(self, table: Table, column_generator: ColumnGenerator):
        self.table = table
        self.colum_generator = column_generator

        self.labels = defaultdict(list)

        for column in self.table.columns:
            for _ in range(table.max_number_of_labels):
                self.labels[column.order].append(
                    self.colum_generator.generate_label(column)
                )

        super().__init__()

    def get_table(self) -> Tuple[str, Iterator[Iterator[str]], str]:
        ## we want this to grow right,
        actual_table = [ [] for _ in self.table.columns ]

        ## we want this to be flat,
        target_table = []

        for column in self.table.columns:
            if self.table.max_number_of_labels == 1:
                choices = self.labels[column.order]
            else:
                n_labels = np.random.randint(1, self.table.max_number_of_labels)

                indexes = list(range(0, len(self.labels[column.order])))
                columns = np.random.choice(indexes, size = n_labels, replace = False)
                choices = [ self.labels[column.order][col] for col in columns ]

            for choice in choices:
                labels = choice[0]
                unit = choice[1]

                actual, expected = self.colum_generator.get_value_for_label(column, labels, unit)

                for row in actual:
                    actual_table[column.order].append(row)

                target_table.append(expected)

        return self.table.get_id(), self.table.compress(actual_table), '\n'.join(target_table)
