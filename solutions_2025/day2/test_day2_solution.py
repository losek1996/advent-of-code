import os

import pytest


from read_data import read_raw_data_without_spaces
from solutions_2025.day2.day2_solution import (
    get_all_invalid_product_ids_sum_first_method,
    IdsRange,
    parse_data,
    get_all_invalid_product_ids_sum_second_method,
)

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> list[IdsRange]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 1227775554),
        pytest.param("data.txt", 21139440284),
    ],
    indirect=["parsed_data"],
)
def test_get_all_invalid_product_ids_sum_first_method(
    parsed_data: list[IdsRange], expected_result: str
) -> None:
    assert get_all_invalid_product_ids_sum_first_method(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param("test_data.txt", 4174379265),
        pytest.param("data.txt", 38731915928),
    ],
    indirect=["parsed_data"],
)
def test_get_all_invalid_product_ids_sum_second_method(
    parsed_data: list[IdsRange], expected_result: str
) -> None:
    assert get_all_invalid_product_ids_sum_second_method(parsed_data) == expected_result
