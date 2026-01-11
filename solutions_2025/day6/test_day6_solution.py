import os

import pytest


from read_data import read_raw_data
from solutions_2025.day6.day6_solution import (
    Problem,
    count_ground_total,
    parse_data,
    parse_data_decomposed_numbers,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[Problem]:
    data = read_raw_data(DATA_DIR + request.param)
    return parse_data(data)


@pytest.fixture
def parsed_data_decomposed_numbers(request) -> list[Problem]:
    data = read_raw_data(DATA_DIR + request.param)
    return parse_data_decomposed_numbers(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 4277556),
        pytest.param("data.txt", 6172481852142),
    ],
    indirect=["parsed_data"],
)
def test_count_ground_total(parsed_data: list[Problem], expected_result: int) -> None:
    assert count_ground_total(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data_decomposed_numbers, expected_result",
    [
        pytest.param("test_data.txt", 3263827),
        pytest.param("data.txt", 10188206723429),
    ],
    indirect=["parsed_data_decomposed_numbers"],
)
def test_count_ground_total(
    parsed_data_decomposed_numbers: list[Problem], expected_result: int
) -> None:
    assert count_ground_total(parsed_data_decomposed_numbers) == expected_result
