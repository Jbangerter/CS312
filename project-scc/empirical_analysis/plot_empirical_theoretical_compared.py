import json
import matplotlib.pyplot as plt


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_prepost_runtimes.json"
    # filename = '_scc_runtimes.json'

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your time complexity
    def big_o_time(v, e):
        return v+e

    # FILL THIS IN from result using compute_coefficient
    coeff = 0.0006023218114935185


    ev, times = zip(*runtimes)

    ee, vv = zip(*ev)

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(vv, ee, times, marker="o")

    predicted_runtime = [coeff * big_o_time(v, e) for (e, v), _ in runtimes]

    # Plot theoretical fit
    ax.plot(vv, ee, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    ax.legend(["Observed", "Theoretical O(V log V + E)"])
    ax.set_xlabel("|V|")
    ax.set_ylabel("|E|")
    ax.set_zlabel("Runtime (ms)")
    ax.set_title("Time for finding Pre and Post Vals")

    # You are welcome to play with the view angle as you'd like
    # elev=0 with azim=0 and azim=90 might be interesting
    ax.view_init(elev=10, azim=-60)

    fig.show()
    fig.savefig("empirical.svg")


if __name__ == "__main__":
    main()
