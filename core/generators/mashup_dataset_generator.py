import random
import numpy as np
from typing import Iterator, Tuple
from ..models.table import Table
from .table_generator import TableGenerator


class MashupDatasetGenerator(object):

    def __init__(self):
        super().__init__()

    def get_data(self, options: Iterator[dict]) -> Iterator[Tuple[str, str]]:
        mashup = None

        for option in options:
            table = option['table']
            dataset = option['dataset_generator'].get_data(table, n_instances = option['n_instances'])
            
            if mashup is None:
                mashup = dataset
            else:
                mashup = np.concatenate([mashup, dataset], axis = 1)

        random.shuffle(mashup)
        return mashup
