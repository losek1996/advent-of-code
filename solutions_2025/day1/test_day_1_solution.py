import os

import pytest


from read_data import read_raw_data_without_spaces
from solutions_2025.day1.day1_solution import (
    Rotations,
    parse_data,
    get_password_first_method,
    get_password_second_method,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> Rotations:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 3),
        pytest.param("data.txt", 1123),
    ],
    indirect=["parsed_data"],
)
def test_get_password_first_method(
    parsed_data: Rotations, expected_result: int
) -> None:
    assert get_password_first_method(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 6),
        pytest.param("data.txt", 6695),
    ],
    indirect=["parsed_data"],
)
def test_get_password_second_method(
    parsed_data: Rotations, expected_result: int
) -> None:
    assert get_password_second_method(parsed_data) == expected_result
