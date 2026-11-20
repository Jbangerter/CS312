# ---------------------------------- Imports --------------------------------- #
from math import inf

from test_utils import assert_valid_tours, run_with_timeout
from utils import Timer, generate_network, score_tour

from byu_pytest_utils import  with_import, tier

# -------------------------------- Test tiers -------------------------------- #

baseline = tier('baseline', 1)
core = tier('core', 2)
stretch1 = tier('stretch1', 3)

# ------------------------------- Baseline tests ------------------------------ #
backtracking_file = "tsp_solve_backtracking"

@baseline
@with_import(backtracking_file)
def test_small_greedy(greedy_tour):
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = greedy_tour(graph, timer)
    assert_valid_tours(graph, stats)

    assert stats[0].tour == [1, 4, 0, 3, 2]
    assert stats[0].score == 21

    assert len(stats) == 1


@baseline
@with_import(backtracking_file)
def test_multiple_solutions_greedy(greedy_tour):
    graph = [
        [0, 1, 2, 3, 4],
        [6, 0, 3, 4, inf],
        [inf, 4, 0, 2, 6],
        [inf, 9, 7, 0, 4],
        [100, 8, 6, 10, 0]
    ]
    timer = Timer(10)
    stats = greedy_tour(graph, timer)
    assert_valid_tours(graph, stats)

    assert len(stats) == 2

    assert stats[0].tour == [0, 1, 2, 3, 4]
    assert stats[0].score == 110

    assert stats[1].tour == [2, 3, 4, 1, 0]
    assert stats[1].score == 22


@baseline
@with_import(backtracking_file)
def test_medium_greedy(greedy_tour):
    locations, edges = generate_network(
        15,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(5)
    stats = greedy_tour(edges, timer)
    assert not timer.time_out()
    assert_valid_tours(edges, stats)
    greedy_score = score_tour(stats[-1].tour, edges)

    assert round(greedy_score, 3) == 3.667


@baseline
@with_import(backtracking_file)
def test_large_greedy(greedy_tour):
    locations, edges = generate_network(
        100,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(5)
    stats = greedy_tour(edges, timer)
    assert not timer.time_out()
    assert_valid_tours(edges, stats)
    greedy_score = score_tour(stats[-1].tour, edges)

    assert round(greedy_score, 3) == 9.757

@baseline
@with_import(backtracking_file)
def test_massive_greedy(greedy_tour):
    locations, edges = generate_network(
        200,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(15)
    stats = greedy_tour(edges, timer)
    assert_valid_tours(edges, stats)

    greedy_score = score_tour(stats[-1].tour, edges)

    assert greedy_score < 16

# ------------------------------- Core tests ------------------------------ #

@core
@with_import(backtracking_file)
def test_tiny_backtracking(backtracking):
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = backtracking(graph, timer)
    assert_valid_tours(graph, stats)

    assert stats[-1].tour == [0, 3, 2, 1, 4]
    assert stats[-1].score == 21


@core
@with_import(backtracking_file)
def test_small_backtracking(backtracking):
    locations, edges = generate_network(
        8,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(30)
    stats = backtracking(edges, timer)
    assert not timer.time_out()
    assert_valid_tours(edges, stats)
    backtracking_score = score_tour(stats[-1].tour, edges)

    assert round(backtracking_score, 3) == 3.224


@core
@with_import(backtracking_file)
def test_medium_backtracking(backtracking):
    locations, edges = generate_network(
        10,
        euclidean=True,
        reduction=0.5,
        normal=False,
        seed=312
    )

    timer = Timer(30)

    stats = backtracking(edges, timer)

    assert timer.time() < 35

    assert_valid_tours(edges, stats)
    backtracking_score = score_tour(stats[-1].tour, edges)

    assert round(backtracking_score, 3) == 4.416


@core
def test_large_backtracking():
    # add timeout so that the autograder doesn't crash if implemented improperly
    run_with_timeout(60,_test_large_backtracking)

@with_import(backtracking_file)
def _test_large_backtracking(backtracking):
    locations, edges = generate_network(
        14,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=312
    )

    timer = Timer(30)

    stats = backtracking(edges, timer)

    assert timer.time() < 35

    assert_valid_tours(edges, stats)
    backtracking_score = score_tour(stats[-1].tour, edges)

    assert backtracking_score < 15

# -------------------------------- Stretch 1 tests -------------------------------- #


@stretch1
@with_import(backtracking_file)
def test_smaller_backtracking_with_bssf(backtracking_bssf):
    locations, edges = generate_network(
        12,
        euclidean=True,
        reduction=0,
        normal=False,
        seed=3,
    )

    backtracking_bssf_timer = Timer(30)
    stats_bssf_backtracking = backtracking_bssf(edges, backtracking_bssf_timer)
    assert backtracking_bssf_timer.time() < 35

    assert_valid_tours(edges, stats_bssf_backtracking)


@stretch1
@with_import(backtracking_file)
def test_medium_backtracking_with_bssf(backtracking_bssf):
    locations, edges = generate_network(
        15,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    backtracking_bssf_timer = Timer(30)
    stats_bssf_backtracking = backtracking_bssf(edges, backtracking_bssf_timer)
    assert backtracking_bssf_timer.time() < 35

    assert_valid_tours(edges, stats_bssf_backtracking)


@stretch1
@with_import(backtracking_file,"backtracking_bssf")
@with_import(backtracking_file, "greedy_tour")
def test_medium_bssf_vs_greedy(greedy_tour,backtracking_bssf):
    edges = [
        [  0,   1,   1,   2,   2,  20,  20,  80,  80, 140, 140, 200, 200, 260, 260, 320],
        [  1,   0,   2,   1, inf,   2, inf,  20, inf,  80, inf, 140, inf, 200, inf, 260],
        [  1,   2,   0, inf,   1, inf,   2, inf,  20, inf,  80, inf, 140, inf, 200, inf],
        [  2,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf,  80, inf, 140, inf, 200],
        [  2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf,  80, inf, 140, inf],
        [ 20,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf,  80, inf, 140],
        [ 20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf,  80, inf],
        [ 80,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf,  80],
        [ 80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20, inf],
        [140,  80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf,  20],
        [140, inf,  80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2, inf],
        [200, 140, inf,  80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf,   2],
        [200, inf, 140, inf,  80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1, inf],
        [260, 200, inf, 140, inf,  80, inf,  20, inf,   2, inf,   1, inf,   0, inf,   1],
        [260, inf, 200, inf, 140, inf,  80, inf,  20, inf,   2, inf,   1, inf,   0, 400],
        [320, 260, inf, 200, inf, 140, inf,  80, inf,  20, inf,   2, inf,   1, 400,   0]
    ]

    greedy_timer=Timer(5)
    stats_greedy = greedy_tour(edges,greedy_timer)

    backtracking_bssf_timer = Timer(30)
    stats_bssf_backtracking = backtracking_bssf(edges, backtracking_bssf_timer)
    assert backtracking_bssf_timer.time() < 35

    assert_valid_tours(edges, stats_bssf_backtracking)

    assert stats_greedy[-1].score > stats_bssf_backtracking[-1].score