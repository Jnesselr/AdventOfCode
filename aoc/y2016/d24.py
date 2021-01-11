import itertools
from dataclasses import dataclass, field
from queue import Queue
from typing import FrozenSet, Set, Dict, Iterator

from aoc.util.coordinate import Coordinate
from aoc.util.graph import Graph, Edge
from aoc.util.grid import GridLocation
from aoc.util.inputs import Input
from aoc.util.queue import PriorityQueue


@dataclass(frozen=True)
class SearchAttempt(object):
    steps: int = field(compare=False)
    robot: Coordinate
    keys: FrozenSet[str]


class Y2016D24(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()
        self.starting_coordinate = self.grid.find('0').pop()
        self.all_keys = set(self.grid.find(lambda x: x not in '#.'))

        self.graph: Graph[Coordinate] = Graph[Coordinate]()
        for start, end in itertools.permutations(self.all_keys, r=2):
            path = self.grid.find_path(start, end, *'.0123456789')
            all_open_path = all(self.grid[c] == '.' for c in path[1:-1])
            if all_open_path:
                self.graph.add(start, end, len(path)-1)

    def part1(self):
        result = self._get_min_steps()

        print("Part 1:", result)

    def part2(self):
        result = self._get_min_steps(returning_to_zero=True)

        print("Part 2:", result)

    def _get_min_steps(self, returning_to_zero=False):
        initial_search = SearchAttempt(steps=0, robot=self.starting_coordinate, keys=frozenset({'0'}))
        queue: PriorityQueue[SearchAttempt] = PriorityQueue[SearchAttempt]()
        queue.push(initial_search, initial_search.steps)
        seen: Dict[Coordinate, Set[FrozenSet[str]]] = {}

        all_keys = frozenset([self.grid[c] for c in self.all_keys])

        while not queue.empty:
            search: SearchAttempt = queue.pop()

            if search.keys == all_keys:
                if not returning_to_zero:
                    return search.steps
                if search.robot == self.starting_coordinate:
                    return search.steps

                # Find our way back
                path = self.grid.find_path(search.robot, self.starting_coordinate, *'.0123456789')
                new_steps = search.steps + len(path) - 1
                queue.push(SearchAttempt(new_steps, self.starting_coordinate, search.keys), new_steps)
                continue

            seen.setdefault(search.robot, set()).add(search.keys)

            edge: Edge[Coordinate]
            for edge in self.graph.edges_from(search.robot):
                key = self.grid[edge.end]
                new_steps = search.steps + edge.weight
                new_robot = edge.end
                new_keys = frozenset(search.keys.union({key}))

                new_search = SearchAttempt(new_steps, new_robot, new_keys)

                if new_robot in seen and new_keys in seen[new_robot]:
                    continue

                queue.push(new_search, new_search.steps)


if __name__ == '__main__':
    code = Y2016D24("2016/24.txt")
    code.part1()
    code.part2()
