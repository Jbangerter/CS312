from math import log

from byu_pytest_utils import compute_coefficient


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_prepost_runtimes.json"
    # filename = "_scc_runtimes.json"

    def big_o_time(v, e):
        # FILL THIS IN with your time complexity
        return v+e
    # O(V log V + E)
    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = 350

    compute_coefficient(filename, big_o_time, start, end)


if __name__ == "__main__":
    main()
