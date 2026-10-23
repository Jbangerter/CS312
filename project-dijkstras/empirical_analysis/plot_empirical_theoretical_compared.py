import json
import math

import matplotlib.pyplot as plt


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    # filename = "_linear_pq_runtimes.json"
    filename = "_heap_pq_runtimes.json"

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # FILL THIS IN with your time complexity in terms of v and e
    def big_o_time(v, e):
        # convert e from density to num edges
        e = v * e
        # linear
        # return v**2 + v*e

        # Heap
        return (v + e) * math.log(v) + (v ** 2)

    # FILL THIS IN from result using compute_coefficient
    # linear
    # coeff = 1.320573299897289e-06

    # Heap
    coeff =5.6386129298346694e-08


    ve, times = zip(*runtimes)
    vv, ee = zip(*ve)
    # convert densities to num edges
    ee = list(ee)
    for i in range(len(ee)):
        ee[i] = ee[i] * vv[i]

    # Plot empirical values
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(vv, ee, times, marker="o")

    predicted_runtime = [coeff * big_o_time(v, e) for (v, e), t in runtimes]

    # Plot theoretical fit
    ax.plot(vv, ee, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # Update title, legend, and axis labels as needed
    ax.legend(["Observed", "Theoretical O((V+E)log(V)+V^2)"])
    ax.set_xlabel("|V|")
    ax.set_ylabel("|E|")
    ax.set_zlabel("Runtime (sec)")
    ax.set_title("Time for Dijkstra's With Heap PQ")

    # You are welcome to play with the view angle as you'd like
    # elev=0 with azim=0 and azim=90 might be interesting
    ax.view_init(elev=10, azim=-60)

    fig.show()
    fig.savefig("empirical_heap.svg")


if __name__ == "__main__":
    main()
