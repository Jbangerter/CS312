import multiprocessing.context
import time
from functools import wraps
from multiprocessing import Pool

import pytest


class Timer:
    def __init__(self, time_limit: float = 60):
        self._start_time = time.time()
        self._lap_time = time.time()
        self._time_limit = time_limit

    def time(self) -> float:
        return time.time() - self._start_time

    def lap_time(self) -> float:
        return time.time() - self._lap_time

    def start_lap(self):
        self._lap_time = time.time()

    def timed_out(self):
        return (time.time() - self._start_time) > self._time_limit


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

