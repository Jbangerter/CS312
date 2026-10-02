import itertools
import json
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from graphs import generate_graph
from scc import find_sccs
from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def _scc(graph):
    find_sccs(graph)


def main(input, headers, grouping, scalar):
    measure_runtime(
        _scc,
        input,
        runtime_scalar=scalar,
        preprocessing=generate_graph,
        output_group=grouping,
    )

    with open("_scc_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes, headers)


if __name__ == "__main__":
    densities = [0.25, 0.5, 1.0, 2.0, 3.0]
    sizes = [10, 50, 100, 500, 2000, 4000, 8000]

    iterations = 10
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes, densities) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))
    headers = ["Density", "  V  ", "Time (ms)"]
    grouping = [1, 0]
    scalar = 1000

    main(input_tuples, headers, grouping, scalar)
