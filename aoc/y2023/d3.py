from math import prod

from aoc.util.coordinate import Coordinate
from aoc.util.inputs import Input


class Y2023D3(object):
    def __init__(self, file_name):
        self.engine = Input(file_name).grid()

        self.adjacent_map: dict[Coordinate, list[int]] = {}
        symbol_coords = self.engine.find(lambda x: x != '.' and not x.isdigit())
        for symbol_coords in symbol_coords:
            leftmost_coordinates = set()

            for neighbor_coord in symbol_coords.neighbors8():
                neighbor = self.engine[neighbor_coord]
                if not neighbor.isdigit():
                    continue  # Not a number, completely ignore

                left_coord = neighbor_coord.left()
                left = self.engine[left_coord]
                while left is not None and left.isdigit():
                    neighbor_coord = left_coord
                    left_coord = neighbor_coord.left()
                    left = self.engine[left_coord]

                leftmost_coordinates.add(neighbor_coord)  # neighbor_coord is leftmost coordinate that is still a number

            part_numbers = list()
            for coords in leftmost_coordinates:
                number = int(self.engine[coords])
                coords = coords.right()
                value = self.engine[coords]
                while value is not None and value.isdigit():
                    number = (number * 10) + int(value)
                    coords = coords.right()
                    value = self.engine[coords]
                part_numbers.append(number)

            self.adjacent_map[symbol_coords] = part_numbers

    def part1(self):
        result = sum(sum(x) for x in self.adjacent_map.values())
        print("Part 1:", result)

    def part2(self):
        result = 0

        for symbol_coord, values in self.adjacent_map.items():
            if self.engine[symbol_coord] != '*':
                continue

            if len(values) != 2:
                continue

            result += prod(values)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D3("2023/3.txt")
    code.part1()
    code.part2()
