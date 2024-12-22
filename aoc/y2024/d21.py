import functools
from itertools import product
from typing import Union

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2024D21(object):
    def __init__(self, file_name):
        self._keypad_entries = Input(file_name).lines()

        numeric_grid: Grid[int] = Grid(3, 4)
        numeric_grid[0, 0] = 7
        numeric_grid[1, 0] = 8
        numeric_grid[2, 0] = 9
        numeric_grid[0, 1] = 4
        numeric_grid[1, 1] = 5
        numeric_grid[2, 1] = 6
        numeric_grid[0, 2] = 1
        numeric_grid[1, 2] = 2
        numeric_grid[2, 2] = 3
        numeric_grid[1, 3] = 0
        numeric_grid[2, 3] = 0xA
        numeric_graph = numeric_grid \
            .to_graph(*numeric_grid.values(), directional=True) \
            .map(lambda c: numeric_grid[c])

        self._numeric_cost_map = {
            (f, t): [
                self._to_directional_string(numeric_grid, p) + 'A'
                for p in numeric_graph.flood_find_all(f, t)
            ]
            for f, t in product(range(11), repeat=2)
        }

        # numeric_grid.print(key=lambda k: hex(k)[2:].upper(), not_found=' ')

        directional_grid: Grid[str] = Grid(3, 2)
        directional_grid[1, 0] = '^'
        directional_grid[2, 0] = 'A'
        directional_grid[0, 1] = '<'
        directional_grid[1, 1] = 'v'
        directional_grid[2, 1] = '>'
        directional_graph = directional_grid \
            .to_graph(*directional_grid.values(), directional=True) \
            .map(lambda c: directional_grid[c])

        self._directional_cost_map = {
            (f, t): [
                self._to_directional_string(directional_grid, p) + 'A'
                for p in directional_graph.flood_find_all(f, t)
            ]
            for f, t in product('^v<>A', repeat=2)
        }

        # directional_grid.print(not_found=' ')

    def part1(self):
        result = 0
        for numpad_entry in self._keypad_entries:
            entry_cost = self._get_entry_cost(numpad_entry, 2)
            result += entry_cost

        print("Part 1:", result)

    def part2(self):
        result = 0
        for numpad_entry in self._keypad_entries:
            entry_cost = self._get_entry_cost(numpad_entry, 25)
            result += entry_cost

        print("Part 2:", result)

    def _get_entry_cost(self, numpad_entry: str, robot_levels: int) -> int:
        keypad_cost = self._keypad_cost(numpad_entry, robot_levels)

        return keypad_cost * int(numpad_entry[:-1])

    @functools.cache
    def _keypad_cost(self, numpad_entry: str, robot_levels: int) -> int:
        numpad_entry = 'A' + numpad_entry

        result = sum(
            min(self._directional_cost(p, robot_levels - 1)
                for p in self._numeric_cost_map[int(f, 16), int(t, 16)]
                )
            for f, t in zip(numpad_entry, numpad_entry[1:])
        )

        return result

    @functools.cache
    def _directional_cost(self, directional_entry: str, robot_level: int) -> int:
        directional_entry = 'A' + directional_entry
        if robot_level == 0:
            result = sum(
                min(len(p) for p in self._directional_cost_map[f, t])
                for f, t in zip(directional_entry, directional_entry[1:])
            )
            return result

        result = sum(
            min(self._directional_cost(p, robot_level - 1) for p in self._directional_cost_map[f, t])
            for f, t in zip(directional_entry, directional_entry[1:])
        )
        return result

    @staticmethod
    def _to_directional_string(grid: Grid, path: Union[list, tuple]) -> str:
        current_coordinate = grid.find(path[0])[0]
        result = ''

        for item in path[1:]:
            next_coordinate = grid.find(item)[0]
            direction_str = {
                current_coordinate.left(): '<',
                current_coordinate.right(): '>',
                current_coordinate.up(): '^',
                current_coordinate.down(): 'v',
            }[next_coordinate]
            result += direction_str

            current_coordinate = next_coordinate

        return result


if __name__ == '__main__':
    code = Y2024D21("2024/21.txt")
    code.part1()
    code.part2()
