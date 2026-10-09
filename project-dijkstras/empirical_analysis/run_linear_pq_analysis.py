import itertools
import json
import os
import random
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from network_routing import find_shortest_path_with_linear_pq

from main import generate_graph
from time import time_ns

from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def _preprocessing(size, density):
    seed = 312
    noise = 0.05

    _, graph = generate_graph(seed, size, density, noise)

    random.seed(time_ns())

    source = 0
    target = random.randint(1, len(graph) - 1)

    return graph, source, target


def _linear_pq(graph, source, target):
    find_shortest_path_with_linear_pq(graph, source, target)


def main(input, recursion_limit, error_message):
    measure_runtime(
        _linear_pq,
        input,
        recursion_limit=recursion_limit,
        preprocessing=_preprocessing,
        error_message=error_message,
    )

    with open("_linear_pq_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes, ["Size", "Density", "Time (sec)"])


if __name__ == "__main__":
    sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    densities = [0.2]

    recursion_limit = sizes[-1] * 2

    error_message = 'An error has occurred. For more information, see "Using the Empirical Analysis Scripts" on Canvas'

    iterations = 10
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes, densities) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))

    main(input_tuples, recursion_limit, error_message)
