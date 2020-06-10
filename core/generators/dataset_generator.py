import numpy as np
from typing import Iterator, Tuple
from .table_generator import TableGenerator


class DatasetGenerator(object):

    def __init__(self):
        super().__init__()

    def get_data(self, table_generator: TableGenerator, n_instances: int) ->  Iterator[Tuple[str, str, str]]:
        dataset = []
        for _ in range(n_instances):
            table_id, train, target = table_generator.get_table()

            dataset.append(
                (
                    table_id,
                    '\n'.join(train).strip('\n'),
                    target.strip('\n')
                )
            )

        return dataset
