import pytest

"""
The three lists below are tuples of inputs and the corresponding answer for each of the exam questions.
"""

from pointBexam import max_number_divby3, min_knight_moves, min_cubicle_path

divby3_test_cases_l = [
    ([3, 1, 4, 1], 4311),
    ([3, 1, 4, 1, 5, 9], 94311),
    ([1, 7], 0)  # no solution case
]
min_knight_moves_test_cases_l = [
    (19, 36, 1),
    (0, 1, 3),
]
min_cubicle_path_l = [
    ([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]], 7),
    ([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1],
      [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]], 11)
]


# pytest decorators
@pytest.mark.parametrize('num_list, answer', divby3_test_cases_l)
def test_problem1_output(num_list, answer):
    assert max_number_divby3(num_list) == answer


@pytest.mark.parametrize('src, dest, answer', min_knight_moves_test_cases_l)
def test_problem2_output(src, dest, answer):
    assert min_knight_moves(src, dest) == answer


@pytest.mark.parametrize('map_grid, answer', min_cubicle_path_l)
def test_problem3_output(map_grid, answer):
    assert min_cubicle_path(map_grid) == answer
