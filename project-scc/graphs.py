import math
import random
from random import gammavariate, sample


def _get_neighbor(i, n, density_factor) -> int:
    step = random.gauss(0, n ** (0.15 * density_factor))

    # Round up, respecting sign
    step = math.copysign(math.ceil(abs(step)), step)

    candidate = i + int(step)
    if candidate > n:
        candidate -= n

    elif candidate < 0:
        candidate += n

    if candidate == 0:
        candidate = 1

    if i == 1 and candidate == i:
        candidate += 1

    elif i == n and candidate == i:
        candidate -= 1

    return candidate


def generate_graph(n: int, density_factor: float) -> dict[str, list[str]]:
    graph = {}

    for i in range(1, n + 1):
        node = f"n{i:0{len(str(n))}d}"
        num_edges = min(n, math.ceil(gammavariate(1.5, 2.0 * density_factor)))
        neighbors = {
            f"n{_get_neighbor(i, n, density_factor):0{len(str(n))}d}"
            for _ in range(num_edges)
        }
        graph[node] = list(sorted(neighbors))

    return graph
