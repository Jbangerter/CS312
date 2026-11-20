import json
import matplotlib.pyplot as plt


def main():

    filename = "_greedy_runtimes.json"

    with open(filename, "r") as f:
        greedy_runtimes = json.load(f)

    filename = "_backtracking_runtimes.json"

    with open(filename, "r") as f:
        backtracking_runtimes = json.load(f)

    g_NN, g_times = zip(*greedy_runtimes)
    g_nn = [n[0] for n in g_NN]

    b_NN, b_times = zip(*backtracking_runtimes)
    b_nn = [n[0] for n in b_NN]

    fig = plt.figure()
    plt.scatter(g_nn, g_times, marker="o")
    plt.plot(g_nn, g_times, c="k", lw=2, label="Greedy")

    plt.scatter(b_nn, b_times, marker="o")
    plt.plot(b_nn, b_times, c="r", lw=2, label="Backtracking")

    plt.legend()
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("Greedy vs. Backtracking Runtime")

    fig.show()
    fig.savefig("greedy_v_backtracking.svg")


if __name__ == "__main__":
    main()
