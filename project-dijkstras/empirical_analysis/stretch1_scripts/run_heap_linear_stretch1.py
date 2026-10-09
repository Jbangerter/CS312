import itertools
import json
import os
import random
import sys
from time import time_ns

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))
sys.path.append(os.path.join(this_folder, "..", ".."))

from main import generate_graph
from network_routing import (
    find_shortest_path_with_linear_pq,
    find_shortest_path_with_heap,
)

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


def _heap_low(graph, source, target):
    find_shortest_path_with_heap(graph, source, target)


def _heap_high(graph, source, target):
    find_shortest_path_with_heap(graph, source, target)


def _linear_low(graph, source, target):
    find_shortest_path_with_linear_pq(graph, source, target)


def _linear_high(graph, source, target):
    find_shortest_path_with_linear_pq(graph, source, target)


def main(low_input, high_input, recursion_limit, error_message):

    print()
    print("Beginning heap with low density")
    measure_runtime(
        _heap_low,
        low_input,
        recursion_limit=recursion_limit,
        preprocessing=_preprocessing,
        error_message=error_message,
    )

    print()
    print("Beginning heap with high density")
    measure_runtime(
        _heap_high,
        high_input,
        recursion_limit=recursion_limit,
        preprocessing=_preprocessing,
        error_message=error_message,
    )

    print()
    print("Beginning linear with low density")
    measure_runtime(
        _linear_low,
        low_input,
        recursion_limit=recursion_limit,
        preprocessing=_preprocessing,
        error_message=error_message,
    )

    print()
    print("Beginning linear with high density")
    measure_runtime(
        _linear_high,
        high_input,
        recursion_limit=recursion_limit,
        preprocessing=_preprocessing,
        error_message=error_message,
    )

    # Low density
    with open("_linear_low_runtimes.json", "r") as ll_file:
        ll_runtimes = json.load(ll_file)

    with open("_heap_low_runtimes.json", "r") as hl_file:
        hl_runtimes = json.load(hl_file)

    ll_ave_runtimes = compute_average_runtimes(ll_runtimes)
    hl_ave_runtimes = compute_average_runtimes(hl_runtimes)

    ll_vv, ll_ee, ll_times = zip(*ll_ave_runtimes)

    _, _, hl_times = zip(*hl_ave_runtimes)

    low_combined = zip(ll_vv, ll_ee, hl_times, ll_times)

    # High density
    with open("_linear_high_runtimes.json", "r") as lh_file:
        lh_runtimes = json.load(lh_file)

    with open("_heap_high_runtimes.json", "r") as hh_file:
        hh_runtimes = json.load(hh_file)

    lh_ave_runtimes = compute_average_runtimes(lh_runtimes)
    hh_ave_runtimes = compute_average_runtimes(hh_runtimes)

    lh_vv, lh_ee, lh_times = zip(*lh_ave_runtimes)

    _, _, hh_times = zip(*hh_ave_runtimes)

    high_combined = zip(lh_vv, lh_ee, hh_times, lh_times)

    print_markdown_table(
        low_combined, ["V   ", "Density", "heap time (sec)", "linear PQ time (sec)"]
    )

    print()

    print_markdown_table(
        high_combined, ["V   ", "Density", "heap time (sec)", "linear PQ time (sec)"]
    )

    print()

    # Print runtimes to a file
    this_folder = os.path.dirname(__file__)
    filename = "_stretch1_linear_runtimes.bk.json"
    runtimes_file = os.path.join(this_folder, filename)
    with open(runtimes_file, "w") as file:
        combined = [ll_ave_runtimes, lh_ave_runtimes]
        json.dump(combined, file, indent=4)

    print()
    print(runtimes_file, "written")

    this_folder = os.path.dirname(__file__)
    filename = "_stretch1_heap_runtimes.bk.json"
    runtimes_file = os.path.join(this_folder, filename)
    with open(runtimes_file, "w") as file:
        combined = [hl_ave_runtimes, hh_ave_runtimes]
        json.dump(combined, file, indent=4)

    print()
    print(runtimes_file, "written")


if __name__ == "__main__":
    sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    low_density = [0.6]
    high_density = [1.0]

    iterations = 3
    low_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes, low_density) for _ in range(iterations)
    )
    low_tuples = sorted(list(low_tuples_iterator))

    high_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes, high_density) for _ in range(iterations)
    )
    high_tuples = sorted(list(high_tuples_iterator))

    recursion_limit = sizes[-1] * 2

    error_message = 'An error has occurred. For more information, see "Using the Empirical Analysis Scripts" on Canvas'

    main(low_tuples, high_tuples, recursion_limit, error_message)
