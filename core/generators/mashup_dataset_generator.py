import pandas as pd
from typing import Iterator
from .dataset_generator import DatasetGenerator


class MashupDatasetGenerator(object):

    def __init__(self):
        self.dataset_generator = DatasetGenerator()

        super().__init__()

    def get_data(self, options: Iterator[dict]) -> pd.DataFrame:
        mashup = []

        for option in options:
            n_instances = option['n_instances']
            dataset = self.dataset_generator.get_data(
                option['table_generator'],
                n_instances = n_instances
            )

            assert len(dataset) == n_instances, f'{len(dataset)} expected {n_instances}'

            for row in dataset:
                mashup.append(row)

        df = pd.DataFrame(mashup)
        df.columns = ['table_id', 'table', 'target']

        return df
