import matplotlib.pyplot as plt
import os
import sys

this_folder = os.path.dirname(__file__)
sys.path.append(os.path.join(this_folder, ".."))

from tsp_solve_backtracking import (
    backtracking,
    backtracking_bssf,
    greedy_tour,
    random_tour,
)

from utils import generate_network, Timer


def main():
    random_times = []
    random_scores = []

    greedy_times = []
    greedy_scores = []

    backtracking_times = []
    backtracking_scores = []

    bssf_times = []
    bssf_scores = []

    _, edges = generate_network(15, euclidean=True, reduction=0, normal=False, seed=312)

    print(f"Begin random")
    timer = Timer(30)
    random_results = random_tour(edges, timer)

    print(f"Begin greedy")
    timer = Timer(30)
    greedy_results = greedy_tour(edges, timer)

    print(f"Begin backtracking")
    timer = Timer(30)
    backtracking_results = backtracking(edges, timer)

    print(f"Begin BSSF")
    timer = Timer(30)
    bssf_results = backtracking_bssf(edges, timer)

    for result in random_results:
        random_times.append(result.time)
        random_scores.append(result.score)

    for result in greedy_results:
        greedy_times.append(result.time)
        greedy_scores.append(result.score)

    for result in backtracking_results:
        backtracking_times.append(result.time)
        backtracking_scores.append(result.score)

    for result in bssf_results:
        bssf_times.append(result.time)
        bssf_scores.append(result.score)

    fig = plt.figure()

    plt.scatter(random_times, random_scores, marker="o", c="k")
    plt.plot(random_times, random_scores, c="k", lw=2, label="Random")

    plt.scatter(greedy_times, greedy_scores, marker="o", c="r")
    plt.plot(greedy_times, greedy_scores, c="r", lw=2, label="Greedy")

    plt.scatter(backtracking_times, backtracking_scores, marker="o", c="y")
    plt.plot(
        backtracking_times,
        backtracking_scores,
        c="y",
        lw=2,
        label="Backtracking",
    )

    plt.scatter(bssf_times, bssf_scores, marker="o", c="g")
    plt.plot(bssf_times, bssf_scores, c="g", lw=2, label="BSSF")

    plt.legend()
    plt.xlabel("Solution time (sec)")
    plt.ylabel("Solution score")
    plt.title("TSP Solvers Compared")

    fig.show()
    fig.savefig("time_vs_solution.svg")


if __name__ == "__main__":
    main()
