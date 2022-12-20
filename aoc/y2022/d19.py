import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from queue import Queue
from typing import Dict, Set

from tqdm.auto import tqdm

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Blueprint:
    id: int
    ore_robot_cost: int
    clay_robot_cost: int
    obsidian_robot_cost: tuple[int, int]
    geode_robot_cost: tuple[int, int]

    @property
    def max_ore_cost(self):
        return max(
            self.ore_robot_cost,
            self.clay_robot_cost,
            self.obsidian_robot_cost[0],
            self.geode_robot_cost[0]
        )


@dataclass(frozen=True)
class State:
    blueprint: Blueprint = field(compare=False)

    minutes_remaining: int

    ore_robots: int = field(default=1)
    clay_robots: int = field(default=0)
    obsidian_robots: int = field(default=0)
    geode_robots: int = field(default=0)

    ore: int = field(default=0)
    clay: int = field(default=0)
    obsidian: int = field(default=0)
    geode: int = field(default=0)

    @property
    def next_states(self):
        next_minutes_remaining = self.minutes_remaining - 1

        if next_minutes_remaining < 0:
            return []

        next_ore = self.ore + self.ore_robots
        next_clay = self.clay + self.clay_robots
        next_obsidian = self.obsidian + self.obsidian_robots
        next_geode = self.geode + self.geode_robots

        # Do nothing, just keep mining
        do_nothing_state = State(
            blueprint=self.blueprint,
            minutes_remaining=next_minutes_remaining,
            ore_robots=self.ore_robots,
            clay_robots=self.clay_robots,
            obsidian_robots=self.obsidian_robots,
            geode_robots=self.geode_robots,
            ore=next_ore,
            clay=next_clay,
            obsidian=next_obsidian,
            geode=next_geode
        )

        result = [do_nothing_state]

        # For buying obsidian and geode's if we have enough materials, it does us no good to buy something else or wait

        if self.ore >= self.blueprint.geode_robot_cost[0] and self.obsidian >= self.blueprint.geode_robot_cost[
            1]:
            return [State(
                blueprint=self.blueprint,
                minutes_remaining=next_minutes_remaining,
                ore_robots=self.ore_robots,
                clay_robots=self.clay_robots,
                obsidian_robots=self.obsidian_robots,
                geode_robots=self.geode_robots + 1,
                ore=next_ore - self.blueprint.geode_robot_cost[0],
                clay=next_clay,
                obsidian=next_obsidian - self.blueprint.geode_robot_cost[1],
                geode=next_geode
            )]

        if self.ore >= self.blueprint.obsidian_robot_cost[0] and self.clay >= self.blueprint.obsidian_robot_cost[1]:
            result.append(State(
                blueprint=self.blueprint,
                minutes_remaining=next_minutes_remaining,
                ore_robots=self.ore_robots,
                clay_robots=self.clay_robots,
                obsidian_robots=self.obsidian_robots + 1,
                geode_robots=self.geode_robots,
                ore=next_ore - self.blueprint.obsidian_robot_cost[0],
                clay=next_clay - self.blueprint.obsidian_robot_cost[1],
                obsidian=next_obsidian,
                geode=next_geode
            ))

        # If we're already producing the max ore we can use each turn, don't bother making more
        if self.ore >= self.blueprint.ore_robot_cost and self.ore_robots < self.blueprint.max_ore_cost:
            result.append(State(
                blueprint=self.blueprint,
                minutes_remaining=next_minutes_remaining,
                ore_robots=self.ore_robots + 1,
                clay_robots=self.clay_robots,
                obsidian_robots=self.obsidian_robots,
                geode_robots=self.geode_robots,
                ore=next_ore - self.blueprint.ore_robot_cost,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode
            ))

        # If we're already producing the max clay we can use each turn, don't bother making more
        if self.ore >= self.blueprint.clay_robot_cost and self.clay_robots < self.blueprint.obsidian_robot_cost[1]:
            result.append(State(
                blueprint=self.blueprint,
                minutes_remaining=next_minutes_remaining,
                ore_robots=self.ore_robots,
                clay_robots=self.clay_robots + 1,
                obsidian_robots=self.obsidian_robots,
                geode_robots=self.geode_robots,
                ore=next_ore - self.blueprint.clay_robot_cost,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode
            ))

        return result


class Y2022D19(object):
    blueprint_regex = re.compile(r'Blueprint (\d+)')
    ore_regex = re.compile(r'Each ore robot costs (\d+) ore')
    clay_regex = re.compile(r'Each clay robot costs (\d+) ore')
    obsidian_regex = re.compile(r'Each obsidian robot costs (\d+) ore and (\d+) clay')
    geode_regex = re.compile(r'Each geode robot costs (\d+) ore and (\d+) obsidian')

    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.blueprints: Dict[int, Blueprint] = {}

        for line in lines:
            blueprint_match = self.blueprint_regex.search(line)
            ore_match = self.ore_regex.search(line)
            clay_match = self.clay_regex.search(line)
            obsidian_match = self.obsidian_regex.search(line)
            geode_regex = self.geode_regex.search(line)

            blueprint = Blueprint(
                id=int(blueprint_match.group(1)),
                ore_robot_cost=int(ore_match.group(1)),
                clay_robot_cost=int(clay_match.group(1)),
                obsidian_robot_cost=(int(obsidian_match.group(1)), int(obsidian_match.group(2))),
                geode_robot_cost=(int(geode_regex.group(1)), int(geode_regex.group(2))),
            )
            self.blueprints[blueprint.id] = blueprint

    def _get_best_for_blueprint(self, blueprint_id, minutes_remaining: int) -> int:
        blueprint: Blueprint = self.blueprints[blueprint_id]
        max_number_of_geodes = 0

        initial_state = State(blueprint, minutes_remaining=minutes_remaining)
        seen: set[State] = {initial_state}
        states_to_check: set[State] = {initial_state}

        previous = {}

        should_look_back_two = False  # Only useful for part 2 on the sample input
        should_look_back_one = blueprint_id == 23 or should_look_back_two

        for _ in range(minutes_remaining):
            max_for_geode = defaultdict(lambda: set())
            for state in states_to_check:
                # print(state)

                for next_state in state.next_states:
                    if next_state in seen:
                        continue

                    max_for_geode[next_state.geode].add(next_state)
                    seen.add(next_state)
                    previous[next_state] = state
            max_geode = max(max_for_geode.keys())
            max_number_of_geodes = max(max_number_of_geodes, max_geode)
            states_to_check = max_for_geode[max_geode]

            if max_geode - 1 in max_for_geode and should_look_back_one:
                states_to_check = states_to_check.union(max_for_geode[max_geode - 1])
            if max_geode - 2 in max_for_geode and should_look_back_two:
                states_to_check = states_to_check.union(max_for_geode[max_geode - 2])
            seen = set()

            # checking_state = list(max_for_geode[max_number_of_geodes])[0]

        # print("Checking:")
        # while checking_state in previous:
        #     print(checking_state)
        #     checking_state = previous[checking_state]

        return max_number_of_geodes

    def part1(self):
        result = 0
        for blueprint_id in self.blueprints.keys():
            best_geodes = self._get_best_for_blueprint(blueprint_id, 24)
            # print(blueprint_id, best_geodes)
            result += blueprint_id * best_geodes

        print("Part 1:", result)

    def part2(self):
        result = 1
        for blueprint_id in [1, 2, 3]:
            best_geodes = self._get_best_for_blueprint(blueprint_id, 32)
            # print(blueprint_id, best_geodes)
            result *= best_geodes

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D19("2022/19.txt")
    code.part1()
    code.part2()
