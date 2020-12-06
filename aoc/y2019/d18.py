from dataclasses import dataclass, field
from queue import Queue
from typing import FrozenSet, Dict, Set, Iterator

from aoc.util import alphabet
from aoc.util.coordinate import Coordinate
from aoc.util.grid import Grid, GridLocation
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class SearchAttempt(object):
    steps: int = field(compare=False)
    robots: FrozenSet[Coordinate]
    keys: FrozenSet[str]

    @property
    def walkable(self):
        all_keys = set(alphabet)
        return {'.'} | all_keys | set(key.upper() for key in self.keys)


@dataclass(frozen=True)
class ReachableKey(object):
    steps: int
    location: Coordinate
    key: str


class Y2019D18(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.grid = Grid.from_str(lines)
        self._fill_tunnels()

    def part1(self):
        grid = self.grid.copy()
        result = self._get_all_keys(grid)

        print("Part 1:", result)

    def part2(self):
        grid = self.grid.copy()
        robot = grid.find('@')[0]
        grid[robot] = '#'
        grid[robot.up()] = '#'
        grid[robot.down()] = '#'
        grid[robot.left()] = '#'
        grid[robot.right()] = '#'
        grid[robot.up().left()] = '@'
        grid[robot.up().right()] = '@'
        grid[robot.down().left()] = '@'
        grid[robot.down().right()] = '@'
        result = self._get_all_keys(grid)

        print("Part 2:", result)

    def _get_all_keys(self, grid: Grid[str]):
        all_keys = {}
        robot_positions = set()
        for position, value in grid.items():
            if value == '@':
                robot_positions.add(position)
                grid[position] = '.'
            elif 97 <= ord(value) <= 122:
                all_keys[position] = value

        key_set = frozenset(all_keys.values())

        initial_search = SearchAttempt(steps=0, robots=frozenset(robot_positions), keys=frozenset())

        queue: PriorityQueue[SearchAttempt] = PriorityQueue[SearchAttempt]()
        queue.push(initial_search, initial_search.steps)
        seen: Dict[Coordinate, Set[FrozenSet[str]]] = {}

        while not queue.empty:
            search: SearchAttempt = queue.pop()

            if search.keys == key_set:
                return search.steps

            for robot in search.robots:
                if robot not in seen:
                    seen[robot] = set()

                if search.keys in seen[robot]:
                    continue

                seen[robot].add(search.keys)

                for reachable_key in self._reachable_keys(grid, robot, search.keys):
                    new_steps = search.steps + reachable_key.steps
                    new_robots = set(search.robots)
                    new_robots.remove(robot)
                    new_robots.add(reachable_key.location)
                    new_keys = set(search.keys)
                    new_keys.add(reachable_key.key)

                    new_search = SearchAttempt(steps=new_steps, robots=frozenset(new_robots), keys=frozenset(new_keys))

                    queue.push(new_search, new_search.steps)

        return -1

    @staticmethod
    def _reachable_keys(grid: Grid[str], robot: Coordinate, keys: FrozenSet[str]) -> Iterator[ReachableKey]:
        queue: Queue[GridLocation[int]] = Queue()
        queue.put(GridLocation(robot, 0))
        seen: Set[Coordinate] = {robot}

        while not queue.empty():
            grid_location = queue.get()

            maybe_key: str = grid[grid_location.coordinate]
            if maybe_key.isalpha() and maybe_key.islower() and maybe_key not in keys:
                yield ReachableKey(
                    steps=grid_location.item,
                    location=grid_location.coordinate,
                    key=maybe_key
                )
                continue

            for neighbor in grid_location.coordinate.neighbors():
                if neighbor in seen:
                    continue
                seen.add(neighbor)

                value = grid[neighbor]
                if value == '#':
                    continue

                # '.' tiles, keys, or doors we have keys for all get searched
                if value == '.' or value.islower() or value.lower() in keys:
                    queue.put(GridLocation(neighbor, grid_location.item + 1))

    def _fill_tunnels(self):
        any_filled = True

        filled_count = 0
        while any_filled:
            any_filled = False
            for location, value in self.grid.items():
                if value != '.':
                    continue

                wall_count = 0
                for neighbor in location.neighbors():
                    if self.grid[neighbor] == '#':
                        wall_count += 1

                if wall_count == 3:
                    any_filled = True
                    self.grid[location] = '#'
                    filled_count += 1


if __name__ == '__main__':
    code = Y2019D18("2019/18.txt")
    # code.part1()
    code.part2()
