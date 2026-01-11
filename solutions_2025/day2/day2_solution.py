from typing import TypeAlias, Callable

from pydantic import BaseModel


Id: TypeAlias = int


class IdsRange(BaseModel):
    min_value: Id
    max_value: Id


def parse_data(data: list[str]) -> list[IdsRange]:
    ids_ranges = []
    for line in data:
        ids_ranges_raw = line.split(",")
        for ids_range_raw in ids_ranges_raw:
            min_value, max_value = ids_range_raw.split("-")
            ids_ranges.append(
                IdsRange(min_value=int(min_value), max_value=int(max_value))
            )

    return ids_ranges


def get_all_invalid_product_ids_sum_first_method(ids_ranges: list[IdsRange]) -> Id:
    invalid_ids = []
    for ids_range in ids_ranges:
        invalid_ids.extend(
            generate_product_invalid_ids(ids_range, is_valid_product_id_first_method)
        )

    return sum(invalid_ids)


def get_all_invalid_product_ids_sum_second_method(ids_ranges: list[IdsRange]) -> Id:
    invalid_ids = []
    for ids_range in ids_ranges:
        invalid_ids.extend(
            generate_product_invalid_ids(ids_range, is_valid_product_id_second_method)
        )

    return sum(invalid_ids)


def generate_product_invalid_ids(
    ids_ranges: IdsRange, is_valid_product_id: Callable
) -> list[Id]:
    """Generated arr of numbers represented as strings between min and max value."""
    invalid_ids = []
    current_value = ids_ranges.min_value
    while current_value <= ids_ranges.max_value:
        if not is_valid_product_id(current_value):
            invalid_ids.append(current_value)
        current_value += 1

    return invalid_ids


def is_valid_product_id_first_method(product_id: Id) -> bool:
    """
    Valid product id is if sequence of digits in not repeated:
    - VALID: 2, 12, 123, 191
    - INVALID: 2323, 11
    """
    product_id = str(product_id)
    id_length = len(product_id)
    if id_length % 2 != 0:
        return True

    return product_id[: id_length // 2] != product_id[id_length // 2 :]


def is_valid_product_id_second_method(product_id: Id) -> bool:
    """
    Valid product id is if sequence of digits in not repeated at least twice:
    - VALID: 2, 12, 123, 191
    - INVALID: 2323, 123123123, 42424242
    """
    product_id = str(product_id)
    id_length = len(product_id)
    lengths_to_check = get_all_divisors_of_a_number(id_length)
    if not lengths_to_check:
        return True

    for length in lengths_to_check:
        chunks = chunk_string(product_id, length)
        if all(chunk == chunks[0] for chunk in chunks):
            return False

    return True


def chunk_string(s: str, n: int) -> list[str]:
    """Split string s into strings of length n"""
    return [s[i : i + n] for i in range(0, len(s), n)]


def get_all_divisors_of_a_number(number: int) -> list[int]:
    divisors = []
    for divisor in range(1, number // 2 + 1):
        if number % divisor == 0:
            divisors.append(divisor)

    return divisors
