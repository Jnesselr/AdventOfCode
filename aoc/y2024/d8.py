import itertools
from collections import defaultdict
from itertools import count

from aoc.util.coordinate import BoundingBox, Coordinate
from aoc.util.inputs import Input


class Y2024D8(object):
    def __init__(self, file_name):
        grid = Input(file_name).grid()
        self._bounding_box: BoundingBox = grid.bounding_box
        self._antennas: set[Coordinate] = set()
        self._antenna_map: defaultdict[str, set[Coordinate]] = defaultdict(lambda: set())
        for coordinate, value in grid.items():
            if value == '.':
                continue

            self._antenna_map[value].add(coordinate)
            self._antennas.add(coordinate)

    def part1(self):
        antinodes = set()
        for frequency, antennas in self._antenna_map.items():
            for antenna_a, antenna_b in itertools.combinations(antennas, r=2):
                antinode_a = antenna_a + (antenna_a - antenna_b)
                antinode_b = antenna_b + (antenna_b - antenna_a)
                if antinode_a in self._bounding_box:
                    antinodes.add(antinode_a)
                if antinode_b in self._bounding_box:
                    antinodes.add(antinode_b)
        result = len(antinodes)

        print("Part 1:", result)

    def part2(self):
        antinodes = set()

        for frequency, antennas in self._antenna_map.items():
            for antenna_a, antenna_b in itertools.combinations(antennas, r=2):
                diffs = [
                    (antenna_a - antenna_b),
                    (antenna_b - antenna_a),
                ]
                for diff in diffs:
                    for i in count():
                        antinode = antenna_a + (diff * i)
                        if antinode not in self._bounding_box:
                            break

                        antinodes.add(antinode)

        result = len(antinodes)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2024D8("2024/8.txt")
    code.part1()
    code.part2()
