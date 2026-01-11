import os

import pytest

from solutions_2022.day19.day19_solution import (
    parse_data,
    OreRobot,
    ClayRobot,
    ObsidianRobot,
    GeodeRobot,
    BluePrintId,
    RobotType,
    RobotCost,
    determine_quality_level_for_all_blueprints,
    get_quality_level_for_all_blueprints,
)
from read_data import read_raw_data_without_spaces

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data/"


@pytest.fixture
def parsed_data(request) -> dict[BluePrintId, dict[RobotType, RobotCost]]:
    data = read_raw_data_without_spaces(DATA_DIR + request.param)
    return parse_data(data)


def test_parse_data() -> None:
    assert parse_data(
        [
            "Blueprint 1: Each ore robot costs 4 ore. "
            "Each clay robot costs 2 ore. "
            "Each obsidian robot costs 3 ore and 14 clay. "
            "Each geode robot costs 2 ore and 7 obsidian."
        ]
    ) == {
        1: {
            OreRobot: RobotCost(ore=4),
            ClayRobot: RobotCost(ore=2),
            ObsidianRobot: RobotCost(ore=3, clay=14),
            GeodeRobot: RobotCost(ore=2, obsidian=7),
        }
    }


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [pytest.param("my_data.txt", 93)],
    indirect=["parsed_data"],
)
def test_determine_quality_level_for_all_blueprints(
    parsed_data: dict[BluePrintId, dict[RobotType, RobotCost]], expected_result: int
) -> None:
    assert determine_quality_level_for_all_blueprints(parsed_data) == expected_result


@pytest.mark.parametrize(
    "parsed_data, expected_result",
    [
        pytest.param(
            "data.txt",
            {
                1: 1,
                2: 4,
                3: 18,
                4: 0,
                5: 0,
                6: 0,
                7: 7,
                8: 0,
                9: 45,
                10: 90,
                11: 66,
                12: 0,
                13: 13,
                14: 42,
                15: 45,
                16: 64,
                17: 153,
                18: 90,
                19: 38,
                20: 20,
                21: 252,
                22: 22,
                23: 23,
                24: 120,
                25: 75,
                26: 0,
                27: 0,
                28: 168,
                29: 203,
                30: 0,
            },
        )
    ],
    indirect=["parsed_data"],
)
def test_get_quality_level_for_all_blueprints(
    parsed_data: dict[BluePrintId, dict[RobotType, RobotCost]], expected_result: int
) -> None:
    assert get_quality_level_for_all_blueprints(parsed_data) == expected_result
