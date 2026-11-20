import math
import multiprocessing.context
import pytest

from multiprocessing import Pool
from utils import score_tour


def assert_valid_tour(edges, tour):
    """
    Length is number of vertices
    Not vertices repeated
    Non-infinite score
    """
    assert len(tour) == len(edges)
    assert len(tour) == len(set(tour))
    assert not math.isinf(score_tour(tour, edges))


def assert_valid_tours(edges, stats):
    assert len(stats) > 0
    for stat in stats:
        assert_valid_tour(edges, stat.tour)

# modified from https://www.reddit.com/r/Python/comments/8t9bk4/the_absolutely_easiest_way_to_time_out_a_function/
def run_with_timeout(seconds, func, *args, **kwargs):
    """
    Calls any function with timeout after 'seconds'.
    """

    p = Pool(processes=1)
    res = p.apply_async(func=func, args=args, kwds=kwargs)
    p.close()

    try:
        return res.get(timeout=seconds)

    except multiprocessing.context.TimeoutError:
        pytest.fail(f"'{func.__name__}' took more than {seconds} seconds to run.")

    finally:
        p.terminate()
        p.join()
