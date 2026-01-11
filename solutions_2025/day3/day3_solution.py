from typing import TypeAlias


BankBatteries: TypeAlias = str
Joltage: TypeAlias = int

JOLTAGE_DIGITS_1ST_METHOD = 2
JOLTAGE_DIGITS_2ND_METHOD = 12


def get_largest_possible_joltage(
    bank_batteries_list: list[BankBatteries], joltage_digits: int
) -> Joltage:
    maximum_joltage_sum = 0
    for bank_battery in bank_batteries_list:
        maximum_joltage_sum += get_bank_battery_maximum_joltage(
            bank_battery, joltage_digits
        )

    return maximum_joltage_sum


def get_largest_possible_joltage_first_method(
    bank_batteries_list: list[BankBatteries],
) -> Joltage:
    return get_largest_possible_joltage(bank_batteries_list, JOLTAGE_DIGITS_1ST_METHOD)


def get_largest_possible_joltage_second_method(
    bank_batteries_list: list[BankBatteries],
) -> Joltage:
    return get_largest_possible_joltage(bank_batteries_list, JOLTAGE_DIGITS_2ND_METHOD)


def get_bank_battery_maximum_joltage(
    bank_batteries: BankBatteries, joltage_digits: int
) -> Joltage:
    output = ""
    start_position = 0
    for idx in range(1, joltage_digits + 1):
        digit, position = get_maximum_digit(
            bank_batteries,
            start_position,
            last_n_positions_to_skip=joltage_digits - idx,
        )
        output += digit
        start_position = position + 1

    return int(output)


def get_maximum_digit(
    s: str, start_position: int, last_n_positions_to_skip: int
) -> tuple[str, int]:
    """Finds maximum digit and its position in string. Skips last n positions."""
    current_position = start_position
    max_digit, max_digit_position = "-1", -1
    while current_position < len(s) - last_n_positions_to_skip:
        current_digit = s[current_position]
        if current_digit > max_digit:
            max_digit = s[current_position]
            max_digit_position = current_position
            if max_digit == 9:
                return "9", max_digit_position
        current_position += 1

    return max_digit, max_digit_position
