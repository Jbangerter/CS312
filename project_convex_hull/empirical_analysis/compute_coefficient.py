from byu_pytest_utils import compute_coefficient
import math


def main():

    filename = "_dvcq_convex_hull_runtimes.json"
    # filename = "_other_convex_hull_runtimes.json"

    def big_o_time(n):
        # FILL THIS IN with your time complexity
        return n * math.log(n) #dvcq      0.000782241712067671
        # return n**2 #other                  3.6694900000776567e-05

    # Changing these values takes a slice of your runtimes corresponding with the indices

    start = None
    end = None

    compute_coefficient(filename, big_o_time, start, end)


if __name__ == "__main__":
    main()
