import pandas as pd
import numpy as np
from typing import Dict, Iterator, Tuple

from ..models import unit
from ..models.column import Column
from ..models.table import Table

from ..generators.label_generator import LabelGenerator
from ..generators.unit_generator import UnitGenerator
from ..generators.column_generator import ColumnGenerator
from ..generators.table_generator import TableGenerator
from ..generators.dataset_generator import DatasetGenerator

from core.generators.mashup_dataset_generator import MashupDatasetGenerator


## Many-to-Many - Same input / output
class ManyToManySameInputAndOutputVocabOrchestrator(object):

    def __init__(self, vocab: str, unit_lookup: Dict[int, str]):
        assert len(vocab) > 0

        self.vocab = [ char for char in vocab ]

        system_vocab = ['\n', ' ', '<eol>'] + [ char for char in '0123456789.\/' ]
        for v in system_vocab:
            self.vocab.append(v)

        self.vocab = list(sorted(set(self.vocab)))

        self.index_to_char = dict([ (i, c) for i, c in enumerate(self.vocab) ])
        self.char_to_index = dict([ (c, i) for i, c in enumerate(self.vocab) ])

        self.unit_lookup = unit_lookup

        label_generator_index_to_char = self.index_to_char.copy()
        for key in system_vocab:
            del label_generator_index_to_char[self.char_to_index[key]]

        self.generators = {
          'label': LabelGenerator(label_generator_index_to_char),
          'unit': UnitGenerator(self.unit_lookup),
        }

        self.generators['column'] = ColumnGenerator(
          self.generators['label'],
          self.generators['unit']
        )

        super().__init__()

    def create_table_generator(self, table: Table):
        return TableGenerator(table, self.generators['column'])

    def get_vocab_size(self):
        return len(self.vocab)

    def build_dataset(self, options: Iterator[dict]):
        ## individual option: { 'table', 'n_instances' }
        return MashupDatasetGenerator().get_data(options)

    def translate_to_string_array(self, input_array: Iterator[int]) -> Iterator[str]:
        return [ self.index_to_char[i] for i in input_array ]

    def translate_to_integer_array(self, dataset: pd.DataFrame, table_lookup: Dict[str, Table]) -> pd.DataFrame:
        def translate(row: str):
            return [ self.char_to_index[char] for char in row ]

        ## 1. calculate the worst possible table,
        ##    - we want to fit a dataset, with different possible tables, into one where the input and output are the exact same.
        table_height = 0
        table_width = 0

        for key in table_lookup:
            table = table_lookup[key]

            calculated_table_width, calculated_table_height = table.get_max_size()

            if calculated_table_width > table_width:
                table_width = calculated_table_width

            if calculated_table_height > table_height:
                table_height = calculated_table_height

        target_total_chars = table_width * table_height

        translated_dataset = []
        for index, row in dataset.iterrows():
            key = row['table_id']

            train = []
            table = table_lookup[key]
            table_splits = row['table'].strip('\n').split('\n')
            for i, table_row in enumerate(table_splits):
                translated_row = translate(table_row)
                if i != 0 and i < len(table_splits) - 1:
                    translated_row = [self.char_to_index['\n']] + translated_row

                if len(translated_row) < table_width:
                    pad = table_width - len(translated_row)
                    translated_row = translated_row + [ self.char_to_index[' '] for _ in range(pad)]

                assert len(translated_row) == table_width, f'{len(translated_row)} <> {table_width}, {index}'
                train.append(translated_row)

            while np.array(train).shape[0] < table_height:
                translated_row = [ self.char_to_index['<eol>'] for _ in range(table_width)]
                train.append(translated_row)

            shape = np.array(train).shape
            assert shape[0] == table_height, f'{shape[0]} <> {table_height}, {index}'

            target = translate(row['target'].strip('\n'))
            if len(target) < target_total_chars:
                pad = target_total_chars - len(target)
                target = target + [ self.char_to_index['<eol>'] for _ in range(pad)]

            assert len(target) == target_total_chars, f'{len(target)} <> {target_total_chars}, {index}'

            translated_dataset.append(
              (np.array(train).flatten().tolist(), target, len(table.columns))
            )

        df = pd.DataFrame(translated_dataset)
        df.columns = ['input', 'output', 'n_columns']

        return df
