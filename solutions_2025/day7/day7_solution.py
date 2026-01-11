from typing import TypeAlias

START_POSITION = "S"
SPLITTER_SIGN = "^"

PathsHistory: TypeAlias = list[list[int]]


def parse_data(data: list[str]) -> list[str]:
    return data


def count_beam_split(data: list[str]) -> tuple[PathsHistory, int]:
    counter = 0
    row_length = len(data[0])
    start_position_idx = data[0].index(START_POSITION)
    current_paths: list[int] = [start_position_idx]
    current_paths_history: list[list[int]] = []

    for row_idx in range(1, len(data)):
        next_paths = []
        current_paths_history.append(current_paths)
        for curr_path in current_paths:
            if data[row_idx][curr_path] == SPLITTER_SIGN:
                new_path = False
                new_path_left = curr_path - 1
                new_path_right = curr_path + 1
                if new_path_left >= 0 and new_path_left not in next_paths:
                    next_paths.append(new_path_left)
                    new_path = True
                if new_path_right < row_length and new_path_right not in next_paths:
                    next_paths.append(new_path_right)
                    new_path = True

                if new_path:
                    counter += 1
            elif curr_path not in next_paths:
                next_paths.append(curr_path)
        current_paths = next_paths

    return current_paths_history, counter


def count_different_timelines(data: list[str]) -> int:
    current_paths_history, _ = count_beam_split(data)
    paths_counter: dict[int, int] = {}
    for path in current_paths_history[0]:
        paths_counter[path] = 1

    for row_idx in range(1, len(current_paths_history)):
        current_path = current_paths_history[row_idx]
        next_paths_counter: dict[int, int] = {}
        for path in current_path:
            if path in paths_counter:
                # Path is being continued
                next_paths_counter[path] = paths_counter[path]

            # We could get to current path from previous left and right paths
            previous_left_path = path - 1
            previous_right_path = path + 1
            if (
                previous_left_path in paths_counter
                and previous_left_path not in current_path
            ):
                next_paths_counter[path] = (
                    next_paths_counter.get(path, 0) + paths_counter[previous_left_path]
                )
            if (
                previous_right_path in paths_counter
                and previous_right_path not in current_path
            ):
                next_paths_counter[path] = (
                    next_paths_counter.get(path, 0) + paths_counter[previous_right_path]
                )
        paths_counter = next_paths_counter

    return sum(paths_counter.values())


def find_start_position_idx(row: str) -> int:
    for idx, char in enumerate(row):
        if char == START_POSITION:
            return idx

    raise StartPositionNotFoundError


class StartPositionNotFoundError(Exception):
    pass
