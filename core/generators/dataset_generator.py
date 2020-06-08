import numpy as np
from typing import Iterator, Tuple
from ..models.table import Table
from .table_generator import TableGenerator


class DatasetGenerator(object):

    def __init__(self, table_generator: TableGenerator):
        self.table_generator = table_generator

        super().__init__()

    def get_data(self, table: Table, n_instances: int) -> Tuple[str, str]:
      dataset = []
      for _ in range(n_instances):
          train, target = self.table_generator.get_table(table)

          dataset.append(
              (
                  '\n'.join(train),
                  target
              )
          )

      return dataset
