import time
from dataclasses import dataclass
from typing import Dict, List, Callable

from aoc.util.coordinate import Coordinate, BoundingBox
from aoc.util.grid import Grid
from aoc.util.inputs import Input


@dataclass(frozen=True)
class CoordinateWithDepth(object):
    coordinate: Coordinate
    depth: int


class Y2019D20(object):
    def __init__(self, file_name):
        self.grid = Grid.from_str(Input(file_name).lines())
        self.portals = self._get_portals()

    def part1(self):
        graph = self.grid.to_graph('.')

        for name, portals in self.portals.items():
            if len(portals) != 2:
                continue

            graph.add(portals[0], portals[1])

        aa = self.portals['AA'][0]
        zz = self.portals['ZZ'][0]

        result = len(graph.flood_find(aa, zz)) - 1

        print("Part 1:", result)

    def part2(self):
        base_graph = self.grid.to_graph('.')

        def with_depth(_depth: int) -> Callable[[Coordinate], CoordinateWithDepth]:
            def _internal(coordinate: Coordinate) -> CoordinateWithDepth:
                return CoordinateWithDepth(coordinate, _depth)

            return _internal

        graph = base_graph.map(with_depth(0))

        for depth in range(40):
            graph.merge(base_graph.map(with_depth(depth)))
            for name, portals in self.portals.items():
                if len(portals) != 2:
                    continue

                start = CoordinateWithDepth(portals[0], depth)
                end = CoordinateWithDepth(portals[1], depth + 1)
                graph.add(start, end)

        aa = CoordinateWithDepth(self.portals['AA'][0], 0)
        zz = CoordinateWithDepth(self.portals['ZZ'][0], 0)

        result = len(graph.flood_find(aa, zz)) - 1

        print("Part 2:", result)

    def _get_portals(self) -> Dict[str, List[Coordinate]]:
        result: Dict[str, List[Coordinate]] = {}
        letters = self.grid.find(lambda ch: ch.isalpha())
        maze_box = BoundingBox().expand(*self.grid.find('#')).shrink()

        for letter_coordinate in letters:
            if self.grid[letter_coordinate.up()] == '.':
                first_letter = self.grid[letter_coordinate]
                second_letter = self.grid[letter_coordinate.down()]
                portal_coordinate = letter_coordinate.up()
            elif self.grid[letter_coordinate.down()] == '.':
                first_letter = self.grid[letter_coordinate.up()]
                second_letter = self.grid[letter_coordinate]
                portal_coordinate = letter_coordinate.down()
            elif self.grid[letter_coordinate.left()] == '.':
                first_letter = self.grid[letter_coordinate]
                second_letter = self.grid[letter_coordinate.right()]
                portal_coordinate = letter_coordinate.left()
            elif self.grid[letter_coordinate.right()] == '.':
                first_letter = self.grid[letter_coordinate.left()]
                second_letter = self.grid[letter_coordinate]
                portal_coordinate = letter_coordinate.right()
            else:
                continue

            portal_name = first_letter + second_letter
            if portal_name not in result:
                result[portal_name] = []
            result[portal_name].append(portal_coordinate)

        # Force the first element to be inside the grid for part 2
        for name in result.keys():
            portals = result[name]
            if len(portals) == 1:
                continue

            if portals[0] not in maze_box:
                result[name] = [portals[1], portals[0]]

        return result


if __name__ == '__main__':
    code = Y2019D20("2019/20.txt")
    # code.part1()
    start = time.time_ns()
    code.part2()
    end = time.time_ns()
    print(end-start)
