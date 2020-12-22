from typing import List

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2018D20(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        start = Coordinate(0, 0)
        grid = self._build_map(start, line)

        walkable = ['X', '.', '|', '-']
        self.flood_map = grid.flood_map(start, *walkable)

    def part1(self):
        result = max(self.flood_map.values()) // 2

        print("Part 1:", result)

    def part2(self):
        result = sum(1 for value in self.flood_map.values() if value >= 2000 and value % 2 == 0)

        print("Part 2:", result)

    @staticmethod
    def _build_map(start, line) -> InfiniteGrid[str]:
        grid: InfiniteGrid[str] = InfiniteGrid[str]()

        stack: List[Coordinate] = []
        current_position = start
        for character in line:
            grid[current_position] = '.'
            for neighbor in current_position.neighbors8():
                if grid[neighbor] is None:
                    grid[neighbor] = '?'

            if character in '^$':
                continue

            if character == 'W':
                west = current_position.left()
                grid[west] = '|'
                current_position = west.left()
            elif character == 'E':
                east = current_position.right()
                grid[east] = '|'
                current_position = east.right()
            elif character == 'N':
                north = current_position.up()
                grid[north] = '-'
                current_position = north.up()
            elif character == 'S':
                south = current_position.down()
                grid[south] = '-'
                current_position = south.down()
            elif character == '(':
                stack.append(current_position)
            elif character == '|':
                current_position = stack[-1]
            elif character == ')':
                current_position = stack.pop()
            else:
                raise ValueError(f"Unknown character {character}")

        to_replace_with_walls = grid.find('?')
        for coordinate in to_replace_with_walls:
            grid[coordinate] = '#'

        grid[start] = 'X'

        return grid





if __name__ == '__main__':
    code = Y2018D20("2018/20.txt")
    code.part1()
    code.part2()
