import itertools
import json
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from alignment import align

from pathlib import Path
from byu_pytest_utils import (
    measure_runtime,
    compute_average_runtimes,
    print_markdown_table,
)


def preprocessing(size):
    seq1_path = Path("../test_files/bovine_coronavirus.txt")
    seq2_path = Path("../test_files/murine_hepatitus.txt")
    seq1 = "".join(seq1_path.read_text().splitlines())[:size]
    seq2 = "".join(seq2_path.read_text().splitlines())[:size]

    return seq1, seq2, 3


def _banded_align(seq1, seq2, banding):
    align(seq1, seq2, banded_width=banding)


def main(input):
    measure_runtime(
        _banded_align,
        input,
        preprocessing=preprocessing,
    )

    with open("_banded_align_runtimes.json", "r") as f:
        runtimes = json.load(f)

    ave_runtimes = compute_average_runtimes(runtimes)

    print_markdown_table(ave_runtimes, [" Size ", "Time (sec)"])


if __name__ == "__main__":
    sizes = [100, 1000, 5000, 10000, 15000, 20000, 25000, 30000]

    iterations = 10
    input_tuples_iterator = itertools.chain.from_iterable(
        itertools.product(sizes) for _ in range(iterations)
    )
    input_tuples = sorted(list(input_tuples_iterator))

    main(input_tuples)
