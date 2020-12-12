from typing import FrozenSet, Set

from aoc.util.coordinate import Coordinate
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2020D11(object):
    def __init__(self, file_name):
        self.grid = Grid.from_str(Input(file_name).lines())

    def part1(self):
        last_state: Set[Coordinate] = set()
        grid = self.grid.copy()
        while True:
            grid = self._mutate1(grid)
            next_state = set(grid.find('#'))
            if last_state == next_state:
                last_state = next_state
                break
            else:
                last_state = next_state

        result = len(last_state)

        print("Part 1:", result)

    @staticmethod
    def _mutate1(grid: Grid[str]) -> Grid[str]:
        new_grid = grid.copy()

        for coordinate, value in grid.items():
            if value == '.':
                continue

            occupied_count = sum([grid[neighbor] == '#' for neighbor in coordinate.neighbors8()])
            if value == 'L' and occupied_count == 0:
                new_grid[coordinate] = '#'
            elif value == '#' and occupied_count >= 4:
                new_grid[coordinate] = 'L'

        return new_grid

    def part2(self):
        last_state: Set[Coordinate] = set()
        grid = self.grid.copy()
        while True:
            grid = self._mutate2(grid)
            next_state = set(grid.find('#'))
            if last_state == next_state:
                last_state = next_state
                break
            else:
                last_state = next_state

        result = len(last_state)

        print("Part 2:", result)

    @classmethod
    def _mutate2(cls, grid: Grid[str]) -> Grid[str]:
        new_grid = grid.copy()

        for coordinate, value in grid.items():
            if value == '.':
                continue

            occupied_count = 0
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.up())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.down())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.left())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.right())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.up().left())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.up().right())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.down().left())
            occupied_count += cls._hits_occupied_seat(grid, coordinate, lambda x: x.down().right())

            if value == 'L' and occupied_count == 0:
                new_grid[coordinate] = '#'
            elif value == '#' and occupied_count >= 5:
                new_grid[coordinate] = 'L'

        return new_grid

    @staticmethod
    def _hits_occupied_seat(grid: Grid[str], starting_coordinate: Coordinate, change) -> bool:
        coordinate = change(starting_coordinate)

        while grid[coordinate] == '.':
            coordinate = change(coordinate)

        return grid[coordinate] == '#'


if __name__ == '__main__':
    code = Y2020D11("2020/11.txt")
    code.part1()
    code.part2()
