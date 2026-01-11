from typing import TypeAlias

from solutions_2022.day9.day9_solution import Position


GridRow: TypeAlias = list[str]
Grid: TypeAlias = list[GridRow]
POSITION: TypeAlias = tuple[int, int]
ROLL_OF_PAPER = "@"
MAX_ALLOWED_ROLLS_OF_PAPER_AROUND = 3
REMOVE_ROLL_OF_PAPER_SIGN = "x"


def parse_data(data: list[str]) -> Grid:
    parsed_data = []
    for row in data:
        parsed_data.append(list(row))
    return parsed_data


def get_num_of_rolls_of_paper_positions_accessible_by_forklift(
    grid: Grid,
) -> int:
    return len(get_roll_of_paper_positions_accessible_by_forklift(grid))


def remove_as_many_rolls_of_paper_as_possible(rows: list[GridRow]) -> int:
    counter = 0
    rolls_of_papers_to_remove = get_roll_of_paper_positions_accessible_by_forklift(rows)

    while rolls_of_papers_to_remove:
        counter += len(rolls_of_papers_to_remove)
        rows = remove_rolls_of_paper_positions(rows, rolls_of_papers_to_remove)
        rolls_of_papers_to_remove = get_roll_of_paper_positions_accessible_by_forklift(
            rows
        )

    return counter


def get_roll_of_paper_positions_accessible_by_forklift(
    grid: Grid,
) -> list[Position]:
    positions = []
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            if row[col_idx] != ROLL_OF_PAPER:
                continue
            roll_of_papers_count = count_rolls_of_papers_around(
                col_idx,
                row,
                previous_row=grid[row_idx - 1] if row_idx - 1 >= 0 else None,
                next_row=grid[row_idx + 1] if row_idx + 1 < len(grid) else None,
            )
            if roll_of_papers_count <= MAX_ALLOWED_ROLLS_OF_PAPER_AROUND:
                positions += [(row_idx, col_idx)]

    return positions


def count_rolls_of_papers_around(
    position: int,
    current_row: GridRow,
    previous_row: GridRow | None,
    next_row: GridRow | None,
) -> int:
    counter = 0
    neighbours = [
        (previous_row, -1),
        (previous_row, 0),
        (previous_row, 1),
        (current_row, -1),
        (current_row, 1),
        (next_row, -1),
        (next_row, 0),
        (next_row, 1),
    ]

    for neighbour_row, neighbour_row_offset in neighbours:
        if neighbour_row is None:
            continue
        neighbour_position = position + neighbour_row_offset
        if (
            0 <= neighbour_position < len(neighbour_row)
            and neighbour_row[neighbour_position] == ROLL_OF_PAPER
        ):
            counter += 1

    return counter


def remove_rolls_of_paper_positions(
    rows: list[GridRow], roll_of_papers_to_remove: list[Position]
) -> list[GridRow]:
    for row_idx, col_idx in roll_of_papers_to_remove:
        print(rows[row_idx][col_idx])
        rows[row_idx][col_idx] = REMOVE_ROLL_OF_PAPER_SIGN

    return rows
