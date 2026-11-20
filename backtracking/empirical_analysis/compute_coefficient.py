from byu_pytest_utils import compute_coefficient


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_greedy_runtimes.json"
    # filename = "_backtracking_runtimes.json"

    def big_o_time(n, _):
        # FILL THIS IN with your time complexity
        return 1

    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = None

    compute_coefficient(filename, big_o_time, start, end)


if __name__ == "__main__":
    main()
