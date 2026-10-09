# ---------------------------------- Imports --------------------------------- #

from main import generate_graph

from byu_pytest_utils import with_import, tier

# -------------------------------- Test tiers -------------------------------- #
baseline = tier('baseline', 1)
core = tier('core', 2)

# ------------------------------- Tests Referenced for Baseline and Core ------------------------------ #

def tiny_test(finder):
    graph = {
        0: {1: 2, 2: 1, 3: 4},
        1: {0: 2, 2: 1, 3: 1},
        2: {0: 4, 1: 4},
        3: {0: 3, 1: 2, 2: 1}
    }
    path, cost = finder(
        graph, 0, 3
    )

    assert path == [0, 1, 3]
    assert cost == 3


def no_path_test(finder):
    _, graph = generate_graph(312, 10, 0.01, 0.05, 'uniform')
    path, cost = finder(graph, 0, 9)
    assert path == []
    assert round(cost, 2) == float('inf')


def small_test(finder):
    _, graph = generate_graph(312, 10, 0.3, 0.05, 'uniform')
    path, cost = finder(graph, 0, 9)
    assert path == [0, 4, 9]
    assert round(cost, 2) == 2.08


def medium_test(finder):
    _, graph = generate_graph(312, 100, 0.02, 0.05, 'uniform')
    path, cost = finder(graph, 4, 52)
    assert path == [4, 76, 84, 83, 52]
    assert round(cost, 2) == 3.77


def large_test(finder):
    _, graph = generate_graph(312, 1000, 0.2, 0.05, 'uniform')
    path, cost = finder(graph, 2, 9)
    assert path == [2, 391, 90, 956, 227, 236, 133, 429, 697, 846, 148, 775, 359, 685, 335, 102, 315, 9]
    assert round(cost, 2) == 1.12


def very_large_test(finder):
    _, graph = generate_graph(312, 1500, 0.2, 0.05)
    path, cost = finder(graph, 9, 2)
    assert path == [9, 308, 1102, 1188, 1127, 313, 751, 1041, 135, 704, 729, 570, 874, 1416,
                    779, 1196, 711, 1125, 539, 865, 506, 1286, 589,42,757, 286, 2]
    assert round(cost, 2) == .78


# ------------------------------- Baseline tests ------------------------------ #
@baseline
@with_import('network_routing')
def test_tiny_network_linear_pq(find_shortest_path_with_linear_pq):
    tiny_test(find_shortest_path_with_linear_pq)


@baseline
@with_import('network_routing')
def test_no_path_network_linear_pq(find_shortest_path_with_linear_pq):
    no_path_test(find_shortest_path_with_linear_pq)


@baseline
@with_import('network_routing')
def test_small_network_linear_pq(find_shortest_path_with_linear_pq):
    small_test(find_shortest_path_with_linear_pq)


@baseline
@with_import('network_routing')
def test_medium_network_linear_pq(find_shortest_path_with_linear_pq):
    medium_test(find_shortest_path_with_linear_pq)


@baseline
@with_import('network_routing')
def test_large_network_linear_pq(find_shortest_path_with_linear_pq):
    large_test(find_shortest_path_with_linear_pq)


@baseline
@with_import('network_routing')
def test_very_large_network_linear_pq(find_shortest_path_with_linear_pq):
    very_large_test(find_shortest_path_with_linear_pq)

# -------------------------------- Core tests -------------------------------- #
@core
@with_import('network_routing')
def test_tiny_network_heap(find_shortest_path_with_heap):
    tiny_test(find_shortest_path_with_heap)


@core
@with_import('network_routing')
def test_no_path_network_heap(find_shortest_path_with_heap):
    no_path_test(find_shortest_path_with_heap)


@core
@with_import('network_routing')
def test_small_network_heap(find_shortest_path_with_heap):
    small_test(find_shortest_path_with_heap)


@core
@with_import('network_routing')
def test_medium_network_heap(find_shortest_path_with_heap):
    medium_test(find_shortest_path_with_heap)


@core
@with_import('network_routing')
def test_large_network_heap(find_shortest_path_with_heap):
    large_test(find_shortest_path_with_heap)


@core
@with_import('network_routing')
def test_very_large_network_heap(find_shortest_path_with_heap):
    very_large_test(find_shortest_path_with_heap)
