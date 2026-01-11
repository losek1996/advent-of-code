import os

import pytest


from read_data import read_raw_data_without_spaces
from solutions_2025.day5.day5_solution import (
    count_available_and_fresh_ingredients,
    parse_data,
    Ingredients,
    count_fresh_ingredients,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> Ingredients:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 3),
        pytest.param("data.txt", 511),
    ],
    indirect=["parsed_data"],
)
def test_count_available_and_fresh_ingredients(
    parsed_data: Ingredients, expected_result: int
) -> None:
    assert count_available_and_fresh_ingredients(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 14),
        pytest.param("data.txt", 350939902751909),
    ],
    indirect=["parsed_data"],
)
def test_count_fresh_ingredients(
    parsed_data: Ingredients, expected_result: int
) -> None:
    assert count_fresh_ingredients(parsed_data) == expected_result
