import os

import pytest


from read_data import read_raw_data_without_spaces
from solutions_2025.day4.day4_solution import (
    get_num_of_rolls_of_paper_positions_accessible_by_forklift,
    GridRow,
    remove_as_many_rolls_of_paper_as_possible,
    parse_data,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[GridRow]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 13),
        pytest.param("data.txt", 1523),
    ],
    indirect=["parsed_data"],
)
def test_get_num_of_rolls_of_paper_positions_accessible_by_forklift(
    parsed_data: list[GridRow], expected_result: int
) -> None:
    assert (
        get_num_of_rolls_of_paper_positions_accessible_by_forklift(parsed_data)
        == expected_result
    )


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 43),
        pytest.param("data.txt", 9290),
    ],
    indirect=["parsed_data"],
)
def test_remove_as_many_rolls_of_paper_as_possible(
    parsed_data: list[GridRow], expected_result: int
) -> None:
    assert remove_as_many_rolls_of_paper_as_possible(parsed_data) == expected_result
