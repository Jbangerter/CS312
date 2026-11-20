import itertools
import json
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from tsp_solve_backtracking import greedy_tour
from utils import generate_network, Timer

from pathlib import Path
from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def _preprocessing(size, reduction):
    _, edges = generate_network(
        size, euclidean=True, reduction=reduction, normal=False, seed=312
    )

    return [edges]


def _greedy(edges):
    timer = Timer(30)
    greedy_tour(edges, timer)


def main(input):
    measure_runtime(
        _greedy,
        input,
        preprocessing=_preprocessing,
    )

    with open("_greedy_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes, ["Size", "Reduction", "Time (sec)"])


if __name__ == "__main__":
    sizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    reduction = [0]

    iterations = 10
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes, reduction) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))

    main(input_tuples)
