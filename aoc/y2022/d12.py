from queue import Queue

from aoc.util.coordinate import Coordinate
from aoc.util.graph import Graph, CoordinateHeuristic
from aoc.util.inputs import Input


class Y2022D12(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()
        self.start: Coordinate = self.grid.find('S')[0]
        self.end: Coordinate = self.grid.find('E')[0]
        self.grid[self.start] = 'a'
        self.grid[self.end] = 'z'

        self.graph = Graph(directional=True)
        for coordinate, value in self.grid.items():
            tests = coordinate.neighbors()

            test: Coordinate
            for test in tests:
                if test not in self.grid:
                    continue

                if ord(self.grid[test]) <= ord(value) + 1:
                    self.graph.add(coordinate, test)

        self.ch = CoordinateHeuristic()

    def part1(self):
        path = self.graph.find_path(self.start, self.end, self.ch)
        result = len(path) - 1

        print("Part 1:", result)

    def part2(self):
        result = 1e24  # Big number is big

        for a_coordinate in self.grid.find('a'):
            path = self.graph.find_path(a_coordinate, self.end, self.ch)
            if path is None:
                continue
            result = min(result, len(path) - 1)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D12("2022/12.txt")
    code.part1()
    code.part2()
