import json
import matplotlib.pyplot as plt


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_unbanded_align_runtimes.json"
    # filename = "_banded_align_runtimes.json"

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your time complexity
    def big_o_time(n):
        return 1

    # FILL THIS IN from result using compute_coefficient
    coeff = 1

    nn, times = zip(*runtimes)

    # Plot empirical values
    fig = plt.figure()
    plt.scatter(nn, times, marker="o")

    predicted_runtime = [coeff * big_o_time(*n) for n, _ in runtimes]

    # Plot theoretical fit
    plt.plot(nn, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    plt.legend(["Observed", "Theoretical O(FILL ME IN)"])
    plt.xlabel("n")
    plt.ylabel("Runtime (sec)")
    plt.title("Time for FILL ME IN")

    # The figure is named after the runtimes file above.
    fig.show()
    fig.savefig(filename.lstrip("_").replace("_runtimes.json", ".svg"))


if __name__ == "__main__":
    main()
