import os

import pytest


from read_data import read_raw_data
from solutions_2025.day7.day7_solution import (
    count_beam_split,
    parse_data,
    count_different_timelines,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[str]:
    data = read_raw_data(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 21),
        pytest.param("data.txt", 1646),
    ],
    indirect=["parsed_data"],
)
def test_count_beam_split(parsed_data: list[str], expected_result: int) -> None:
    _, counter = count_beam_split(parsed_data)
    assert counter == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 40),
        pytest.param("data.txt", 32451134474991),
    ],
    indirect=["parsed_data"],
)
def test_count_different_timelines(
    parsed_data: list[str], expected_result: int
) -> None:
    assert count_different_timelines(parsed_data) == expected_result
