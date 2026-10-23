import json
import matplotlib.pyplot as plt


def main():

    filename = "_stretch1_linear_runtimes.bk.json"

    with open(filename, "r") as f:
        l_runtimes = json.load(f)

    filename = "_stretch1_heap_runtimes.bk.json"
    with open(filename, "r") as f:
        h_runtimes = json.load(f)

    ll_size, _, ll_times = zip(*l_runtimes[0])
    lh_size, _, lh_times = zip(*l_runtimes[1])

    hl_size, _, hl_times = zip(*h_runtimes[0])
    hh_size, _, hh_times = zip(*h_runtimes[1])

    fig = plt.figure()

    plt.plot(
        ll_size,
        ll_times,
        label="Linear with low density",
        c="b",
        lw=2,
        ls="--",
        alpha=0.5,
    )
    plt.plot(
        hl_size,
        hl_times,
        label="Heap with low density",
        c="g",
        lw=2,
        ls="--",
        alpha=0.5,
    )
    plt.plot(
        lh_size,
        lh_times,
        label="Linear with high density",
        c="b",
        lw=2,
        alpha=0.5,
    )
    plt.plot(
        hh_size,
        hh_times,
        label="Heap with high density",
        c="g",
        lw=2,
        alpha=0.5,
    )

    plt.legend()
    plt.xlabel("n")
    plt.ylabel("Runtime")
    plt.title("Linear v. Heap Performance")

    fig.show()
    fig.savefig("stretch1.svg")


if __name__ == "__main__":
    main()
