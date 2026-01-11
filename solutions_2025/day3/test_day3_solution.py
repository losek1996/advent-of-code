import os

import pytest


from read_data import read_raw_data_without_spaces
from solutions_2025.day3.day3_solution import (
    BankBatteries,
    Joltage,
    get_largest_possible_joltage_first_method,
    get_largest_possible_joltage_second_method,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[BankBatteries]:
    return read_raw_data_without_spaces(DATA_DIR + request.param)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 357),
        pytest.param("data.txt", 16854),
    ],
    indirect=["parsed_data"],
)
def test_get_largest_possible_joltage_first_method(
    parsed_data: list[BankBatteries], expected_result: Joltage
) -> None:
    assert get_largest_possible_joltage_first_method(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 3121910778619),
        pytest.param("data.txt", 167526011932478),
    ],
    indirect=["parsed_data"],
)
def test_get_largest_possible_joltage_second_method(
    parsed_data: list[BankBatteries], expected_result: Joltage
) -> None:
    assert get_largest_possible_joltage_second_method(parsed_data) == expected_result
