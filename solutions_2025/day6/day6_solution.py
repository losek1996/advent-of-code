from enum import Enum
from functools import reduce

from pydantic import BaseModel


class Operation(str, Enum):
    ADD = "+"
    MULTIPLY = "*"


AVAILABLE_OPERATIONS = [op.value for op in Operation]


class Problem(BaseModel):
    numbers: list[int]
    operation: Operation = Operation.ADD


def parse_data(data: list[str]) -> list[Problem]:
    problems_to_solve: list[Problem] = []
    last_row_idx = len(data) - 1
    for idx, row in enumerate(data):
        if idx == 0:
            numbers = [int(n) for n in row.split()]
            for number in numbers:
                problems_to_solve.append(
                    Problem(
                        numbers=[number],
                    )
                )
        elif idx < last_row_idx:
            numbers = [int(n) for n in row.split()]
            for i, number in enumerate(numbers):
                problems_to_solve[i].numbers.append(number)
        elif idx == last_row_idx:
            operations = [op for op in row.split()]
            for i, operation in enumerate(operations):
                problems_to_solve[i].operation = Operation(operation)

    return problems_to_solve


def parse_data_decomposed_numbers(data: list[str]) -> list[Problem]:
    problems_to_solve: list[Problem] = []
    longest_row_characters = len(max(data, key=len))
    for curr_idx in range(longest_row_characters):
        last_row_curr = data[-1][curr_idx] if curr_idx < len(data[-1]) else ""
        if last_row_curr in AVAILABLE_OPERATIONS:
            problems_to_solve.append(
                Problem(
                    numbers=[],
                    operation=Operation(last_row_curr),
                )
            )
        number = get_decomposed_number(data, curr_idx)
        if number:
            problems_to_solve[-1].numbers.append(number)

    return problems_to_solve


def count_ground_total(problems: list[Problem]) -> int:
    return sum(get_problem_sum(p.numbers, p.operation) for p in problems)


def get_problem_sum(numbers: list[int], operation: Operation) -> int:
    if operation == Operation.MULTIPLY:
        return reduce(lambda x, y: x * y, numbers)
    elif operation == Operation.ADD:
        return reduce(lambda x, y: x + y, numbers)
    raise OperationNotSupportedError


def get_decomposed_number(data: list[str], curr_idx: int) -> int | None:
    digits = [
        row[curr_idx]
        for row in data[:-1]
        if curr_idx < len(row) and row[curr_idx].isdigit()
    ]
    if not digits:
        return None
    return int("".join(digits))


class OperationNotSupportedError(Exception):
    pass
