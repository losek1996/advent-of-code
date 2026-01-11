import re
import queue
from collections import defaultdict
from typing import NamedTuple

type BluePrintId = int

type OreRobot = "OreRobot"
type ClayRobot = "ClayRobot"
type ObsidianRobot = "ObsidianRobot"
type GeodeRobot = "GeodeRobot"
type RobotType = OreRobot | ClayRobot | ObsidianRobot | GeodeRobot


class RobotCost(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


class CurrentResources(NamedTuple):
    ore: int
    clay: int
    obsidian: int


class OwnedRobotsInfo(NamedTuple):
    """Per each type of robot"""

    owned_robots: int
    current_number_of_resource: int


"""Geode robots don't produce any resource, geode robots just open geodes"""


class State(NamedTuple):
    remaining_time: int
    open_geode: int
    owned_robots: dict[RobotType, OwnedRobotsInfo]


def parse_data(data: list[str]) -> dict[BluePrintId, dict[RobotType, RobotCost]]:
    blueprints = {}
    for row in data:
        matched_input_data = re.match(
            r"^Blueprint (.*?): Each ore robot costs (.*?) ore. Each clay robot costs (.*?) ore. "
            r"Each obsidian robot costs (.*?) ore and (.*?) clay. Each geode robot costs (.*?) ore and (.*?) obsidian.$",
            row,
        )

        blueprint_id = int(matched_input_data.group(1))
        blueprints[blueprint_id] = {
            OreRobot: RobotCost(
                ore=int(matched_input_data.group(2)),
            ),
            ClayRobot: RobotCost(
                ore=int(matched_input_data.group(3)),
            ),
            ObsidianRobot: RobotCost(
                ore=int(matched_input_data.group(4)),
                clay=int(matched_input_data.group(5)),
            ),
            GeodeRobot: RobotCost(
                ore=int(matched_input_data.group(6)),
                obsidian=int(matched_input_data.group(7)),
            ),
        }

    return blueprints


def determine_quality_level_for_all_blueprints(
    parsed_data: dict[BluePrintId, dict[RobotType, RobotCost]],
) -> int:
    quality_levels = get_quality_level_for_all_blueprints(parsed_data)
    return sum(quality_levels.values())


def get_quality_level_for_all_blueprints(
    parsed_data: dict[BluePrintId, dict[RobotType, RobotCost]],
) -> dict[int, int]:
    quality_levels = {
        blueprint_id: determine_quality_level_for_blueprint(
            blueprint_id, robots_with_infos, 24
        )
        for blueprint_id, robots_with_infos in parsed_data.items()
    }
    return quality_levels


def determine_quality_level_for_blueprint(
    blueprint_id: int,
    robots_with_cost: dict[RobotType, RobotCost],
    remaining_time: int,
) -> int:
    max_open_geodes = []
    for number_of_ore_robots in [2]:  #  range(robots_with_cost[ClayRobot].ore):
        max_open_geodes.append(
            find_max_open_geodes_for_blueprint(
                robots_with_cost,
                remaining_time,
                desired_number_of_ore_robots=number_of_ore_robots + 1,
            )
        )

    return max(max_open_geodes) * blueprint_id


def find_max_open_geodes_for_blueprint(
    robots_with_cost: dict[RobotType, RobotCost],
    remaining_time: int,
    desired_number_of_ore_robots: int,
) -> int:
    number_of_geodes_that_can_be_opened_solutions = []
    moves_queue = queue.Queue()
    initial_state: State = State(
        remaining_time=remaining_time,
        open_geode=0,
        owned_robots={
            OreRobot: OwnedRobotsInfo(owned_robots=1, current_number_of_resource=0),
            ClayRobot: OwnedRobotsInfo(owned_robots=0, current_number_of_resource=0),
            ObsidianRobot: OwnedRobotsInfo(
                owned_robots=0, current_number_of_resource=0
            ),
            GeodeRobot: OwnedRobotsInfo(owned_robots=0, current_number_of_resource=0),
        },
    )
    moves_queue.put(initial_state)
    while not moves_queue.empty():
        current_state: State = moves_queue.get()
        if current_state.remaining_time == 0:
            number_of_geodes_that_can_be_opened_solutions.append(
                current_state.open_geode
            )
        else:
            next_moves: list[State] = create_next_moves_heuristic(
                current_state, robots_with_cost, desired_number_of_ore_robots
            )
            for next_move in next_moves:
                if next_move.remaining_time == 9:
                    pass
                    if (
                        next_move.owned_robots[ClayRobot].owned_robots >= 7
                        and next_move.owned_robots[ObsidianRobot].owned_robots >= 1
                    ):
                        pass
                moves_queue.put(next_move)

    return max(
        number_of_geodes_that_can_be_opened_solutions
        if number_of_geodes_that_can_be_opened_solutions
        else [0]
    )


def create_next_moves_heuristic(
    state: State,
    robots_cost: dict[RobotType, RobotCost],
    desired_number_of_ore_robots: int,
) -> list[State]:
    """
    This is close to brute-force implementation with some enhancements:
    - if you can buy Geode or Obsidian, always do so
    """
    if state.remaining_time == 0:
        return []
    current_resources = _get_resources_to_buy_robot_from_state(state)
    """You need to have at least 2 moves to make a profit from buying a robot."""
    if state.remaining_time >= 2:
        robots_to_buy = get_robots_to_buy_heuristic(
            state, current_resources, robots_cost, desired_number_of_ore_robots
        )
    else:
        robots_to_buy = []
    state = _get_updated_state(state, defaultdict(int))
    """If there is a chance to buy a ObsidianRobot or GeodeRobot always do it."""
    if GeodeRobot in robots_to_buy or ObsidianRobot in robots_to_buy:
        robot_type = robots_to_buy[0]
        return [buy_robot(state, robot_type, robots_cost[robot_type])]
    elif OreRobot in robots_to_buy and ClayRobot in robots_to_buy:
        return [
            buy_robot(state, OreRobot, robots_cost[OreRobot]),
            buy_robot(state, ClayRobot, robots_cost[ClayRobot]),
        ]
    elif robots_to_buy == [ClayRobot]:
        # if state.owned_robots[ObsidianRobot].owned_robots == 0:
        return [state, buy_robot(state, ClayRobot, robots_cost[ClayRobot])]
    elif robots_to_buy == [OreRobot]:
        return [buy_robot(state, OreRobot, robots_cost[OreRobot])]
    return [state]


def create_next_moves_brute_force(
    state: State,
    robots_cost: dict[RobotType, RobotCost],
) -> list[State]:
    """
    This is close to brute-force implementation with some enhancements:
    - if you can buy Geode or Obsidian, always do so
    """
    if state.remaining_time == 0:
        return []

    current_resources = _get_resources_to_buy_robot_from_state(state)
    """You need to have at least 2 moves to make a profit from buying a robot."""

    if (
        state.remaining_time <= 10
        and state.owned_robots[ObsidianRobot].owned_robots == 0
    ):
        return []

    if state.remaining_time >= 2:
        robots_to_buy = get_robots_to_buy_brute_force(
            state, current_resources, robots_cost
        )
    else:
        robots_to_buy = []
    state = _get_updated_state(state, defaultdict(int))
    return [
        state,
        *[
            buy_robot(state, robot_type, robots_cost[robot_type])
            for robot_type in robots_to_buy
        ],
    ]


def buy_robot(state: State, robot_type: RobotType, robot_cost: RobotCost) -> State:
    owned_robots = state.owned_robots
    return State(
        remaining_time=state.remaining_time,
        open_geode=state.open_geode,
        owned_robots={
            OreRobot: OwnedRobotsInfo(
                owned_robots=owned_robots[OreRobot].owned_robots
                + (1 if robot_type == OreRobot else 0),
                current_number_of_resource=owned_robots[
                    OreRobot
                ].current_number_of_resource
                - robot_cost.ore,
            ),
            ClayRobot: OwnedRobotsInfo(
                owned_robots=owned_robots[ClayRobot].owned_robots
                + (1 if robot_type == ClayRobot else 0),
                current_number_of_resource=owned_robots[
                    ClayRobot
                ].current_number_of_resource
                - robot_cost.clay,
            ),
            ObsidianRobot: OwnedRobotsInfo(
                owned_robots=owned_robots[ObsidianRobot].owned_robots
                + (1 if robot_type == ObsidianRobot else 0),
                current_number_of_resource=owned_robots[
                    ObsidianRobot
                ].current_number_of_resource
                - robot_cost.obsidian,
            ),
            GeodeRobot: OwnedRobotsInfo(
                owned_robots=owned_robots[GeodeRobot].owned_robots
                + (1 if robot_type == GeodeRobot else 0),
                current_number_of_resource=0,
            ),
        },
    )


def get_robots_to_buy_heuristic(
    state: State,
    current_resources: CurrentResources,
    robots_cost: dict[RobotType, RobotCost],
    desired_number_of_ore_robots: int,
) -> list[RobotType]:
    if state.owned_robots[OreRobot].owned_robots < desired_number_of_ore_robots:
        can_buy_ore_robot = _can_buy_a_robot(current_resources, robots_cost[OreRobot])
        can_buy_clay_robot = _can_buy_a_robot(current_resources, robots_cost[ClayRobot])
        if can_buy_ore_robot and can_buy_clay_robot:
            return [OreRobot, ClayRobot]
        elif can_buy_ore_robot:
            return [OreRobot]
        elif can_buy_clay_robot:
            return [ClayRobot]
        else:
            return []

    for robot_type in [GeodeRobot, ObsidianRobot, ClayRobot]:
        can_buy = _can_buy_a_robot(current_resources, robots_cost[robot_type])
        if can_buy and robot_type == GeodeRobot:
            return [GeodeRobot]
        elif can_buy and robot_type == ObsidianRobot:
            return [ObsidianRobot]
        elif can_buy and robot_type == ClayRobot:
            return [ClayRobot]

    return []


def get_robots_to_buy_brute_force(
    state: State,
    current_resources: CurrentResources,
    robots_cost: dict[RobotType, RobotCost],
) -> list[RobotType]:
    if (
        state.remaining_time <= 8
        and state.owned_robots[ObsidianRobot].owned_robots == 0
    ):
        return []
    robots_to_buy = []
    for robot_type in [GeodeRobot, ObsidianRobot, ClayRobot, OreRobot]:
        if _can_buy_a_robot(current_resources, robots_cost[robot_type]):
            if robot_type == GeodeRobot:
                return [GeodeRobot]
            elif robot_type == ObsidianRobot:
                return [ObsidianRobot]
            else:
                robots_to_buy.append(robot_type)
    return robots_to_buy


def _can_buy_a_robot(
    current_resources: CurrentResources,
    robot_cost: RobotCost,
) -> bool:
    return (
        robot_cost.ore <= current_resources.ore
        and robot_cost.clay <= current_resources.clay
        and robot_cost.obsidian <= current_resources.obsidian
    )


def _get_updated_state(state: State, robots_bought: dict[RobotType, int]) -> State:
    """Collect resources, open geodes"""
    owned_robots_updated = {}

    """We don't collect resources for robots that we just bought."""
    for robot_type in [ObsidianRobot, ClayRobot, OreRobot]:
        owned_robots_number = state.owned_robots[robot_type].owned_robots
        current_number_of_resource = state.owned_robots[
            robot_type
        ].current_number_of_resource
        owned_robots_updated[robot_type] = OwnedRobotsInfo(
            owned_robots=owned_robots_number,
            current_number_of_resource=current_number_of_resource
            + owned_robots_number
            - robots_bought[robot_type],
        )
    owned_robots_updated[GeodeRobot] = state.owned_robots[GeodeRobot]

    return State(
        remaining_time=state.remaining_time - 1,
        open_geode=state.open_geode
        + state.owned_robots[GeodeRobot].owned_robots
        - robots_bought[GeodeRobot],
        owned_robots=owned_robots_updated,
    )


def _get_resources_to_buy_robot_from_state(state: State) -> CurrentResources:
    return CurrentResources(
        ore=state.owned_robots[OreRobot].current_number_of_resource,
        clay=state.owned_robots[ClayRobot].current_number_of_resource,
        obsidian=state.owned_robots[ObsidianRobot].current_number_of_resource,
    )
