from typing import TypeAlias

STARTING_POSITION = 50
MAX_POSITIONS = 100
ZERO_POSITION = 0


Rotations: TypeAlias = list[int]


def parse_data(data: list[str]) -> Rotations:
    rotations = []
    for rotation in data:
        rotations.append(get_rotation(rotation))

    return rotations


def get_rotation(rotation: str) -> int:
    if rotation.startswith("R"):
        return int(rotation[1:])
    elif rotation.startswith("L"):
        return -int(rotation[1:])
    raise IncorrectRotationError(rotation)


def get_password_first_method(rotations: Rotations) -> int:
    how_many_zeros_reached = 0
    current_position = STARTING_POSITION

    for rotation in rotations:
        current_position = (current_position + rotation) % MAX_POSITIONS
        if current_position == ZERO_POSITION:
            how_many_zeros_reached += 1

    return how_many_zeros_reached


def get_password_second_method(rotations: Rotations) -> int:
    how_many_zeros_crossed = 0
    current_position = STARTING_POSITION
    for rotation in rotations:
        how_many_zeros_crossed += abs(rotation) // MAX_POSITIONS
        remainder = abs(rotation) % MAX_POSITIONS
        if rotation > 0 and (remainder + current_position) >= MAX_POSITIONS:
            how_many_zeros_crossed += 1
        elif rotation < 0 and ZERO_POSITION < current_position <= remainder:
            how_many_zeros_crossed += 1

        current_position = (current_position + rotation) % MAX_POSITIONS

    return how_many_zeros_crossed


class IncorrectRotationError(Exception):
    pass
