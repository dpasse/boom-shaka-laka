import math
import pandas as pd


def train_test_dev_split(dataset: pd.DataFrame, percent_allocated_to_training: float):
    assert percent_allocated_to_training < 1 and percent_allocated_to_training > 0

    ## shuffle
    dataset = dataset.sample(frac=1).reset_index(drop=True)

    n_rows = len(dataset)
    pivot = math.floor(n_rows * percent_allocated_to_training)

    train = dataset[:pivot]
    test_and_dev = dataset[pivot:]

    n_train = len(train)
    n_test_and_dev = len(test_and_dev)

    test = []
    dev = []

    if n_test_and_dev >= 2:
        p = n_test_and_dev // 2

        dev = test_and_dev[:p]
        test = test_and_dev[p:]
    else:
        test = test_and_dev

    return (train, dev, test)