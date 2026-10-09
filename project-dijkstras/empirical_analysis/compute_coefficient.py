from byu_pytest_utils import compute_coefficient


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_linear_pq_runtimes.json"
    # filename = "_heap_pq_runtimes.json"

    def big_o_time(v, e):
        # convert e from density to num edges
        e = v * e
        # FILL THIS IN with your theoretical time complexity in terms of v and e
        return 1

    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = None

    compute_coefficient(filename, big_o_time, start, end)


if __name__ == "__main__":
    main()
