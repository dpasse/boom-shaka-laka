import numpy as np
from typing import Iterator


class LabelGenerator(object):

    def __init__(self, index_to_char: dict):
        self.index_to_char = index_to_char
        self.keys = list(self.index_to_char.keys())
        super().__init__()

    def get_label(self, label_length: int) -> str:
        indexes = np.random.choice(self.keys, label_length)
        return ''.join([ self.index_to_char[i] for i in indexes ])

    def get_many_labels(self, min_size: int, max_size: int, n_labels: int) -> Iterator[str]:
        labels = []
        for _ in range(n_labels):
            label_length = np.random.randint(min_size, max_size)
            labels.append(
                self.get_label(label_length)
            )

        return labels
