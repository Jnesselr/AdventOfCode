from dataclasses import dataclass
from typing import Set, Dict, Optional

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


@dataclass
class GridWithBiodiversity(object):
    grid: Grid[str]
    biodiversity: int


class Y2019D24(object):
    def __init__(self, file_name):
        self.base_grid = Grid.from_str(Input(file_name).lines())
        biodiversity = 0
        for col in range(5):
            for row in range(5):
                if self.base_grid[col, row] == '#':
                    index = 5 * row + col
                    biodiversity |= 2**index
        self.with_biodiversity = GridWithBiodiversity(self.base_grid, biodiversity)

    def part1(self):
        current = self.with_biodiversity
        seen: Set[int] = set()
        while current.biodiversity not in seen:
            seen.add(current.biodiversity)
            current = self._mutate(current)

        result = current.biodiversity

        print("Part 1:", result)

    def part2(self):
        grids: Dict[int, Grid[str]] = {0: self.base_grid.copy()}

        for i in range(200):
            grids = self._mutate_recursive(grids)

        result = sum([len(grid.find('#')) for grid in grids.values()])

        print("Part 2:", result)

    @staticmethod
    def _print_grids(grids):
        keys = sorted(grids.keys())
        for key in keys:
            print(f"Depth {key}")
            grids[key].print()
            print()

    @staticmethod
    def _is_infected(current: str, bug_count: int) -> bool:
        if current == '#' and bug_count != 1:
            return False
        elif 1 <= bug_count <= 2:
            return True
        else:
            return current == '#'

    @classmethod
    def _mutate(cls, with_biodiversity: GridWithBiodiversity) -> GridWithBiodiversity:
        grid = with_biodiversity.grid
        result = grid.copy()

        biodiversity = 0
        for coordinate in grid:
            bug_count = grid.neighbor_count(coordinate, '#')

            is_infected = cls._is_infected(grid[coordinate], bug_count)
            result[coordinate] = '#' if is_infected else '.'

            if is_infected:
                index = 5 * coordinate.y + coordinate.x
                biodiversity |= 2 ** index

        return GridWithBiodiversity(result, biodiversity)

    @classmethod
    def _mutate_recursive(cls, grids: Dict[int, Grid[str]]) -> Dict[int, Grid[str]]:
        result: Dict[int, Grid[str]] = {}

        min_level = 2**24
        max_level = -2**24
        for key, grid in grids.items():
            result[key] = grid
            min_level = min(min_level, key)
            max_level = max(max_level, key)

        if len(grids[min_level].find('#')) > 0:
            min_level -= 1
            result[min_level] = grids[0].copy()
            result[min_level].fill('.')

        if len(grids[max_level].find('#')) > 0:
            max_level += 1
            result[max_level] = grids[0].copy()
            result[max_level].fill('.')

        for key, grid in result.items():
            below = grids[key + 1] if key + 1 in grids else None
            above = grids[key - 1] if key - 1 in grids else None
            current = result[key]
            next_grid = result[key].copy()
            for x in range(5):
                for y in range(5):
                    coordinate = Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
                    bug_count = cls._get_bug_count(coordinate, current, above, below)
                    is_infected = cls._is_infected(current[coordinate], bug_count)
                    next_grid[coordinate] = '#' if is_infected else '.'
            result[key] = next_grid

        return result

    @staticmethod
    def _get_bug_count(coordinate: Coordinate,
                       current: Grid[str],
                       above: Optional[Grid[str]],
                       below: Optional[Grid[str]]):
        bug_count = current.neighbor_count(coordinate, '#')
        if coordinate.x == 2 and coordinate.y == 2:
            return 0  # Center location is another grid, so keep the state of empty.

        if below is not None:
            if coordinate.x == 2 and coordinate.y == 1:
                bug_count += 1 if below[0, 0] == '#' else 0
                bug_count += 1 if below[1, 0] == '#' else 0
                bug_count += 1 if below[2, 0] == '#' else 0
                bug_count += 1 if below[3, 0] == '#' else 0
                bug_count += 1 if below[4, 0] == '#' else 0
            elif coordinate.x == 1 and coordinate.y == 2:
                bug_count += 1 if below[0, 0] == '#' else 0
                bug_count += 1 if below[0, 1] == '#' else 0
                bug_count += 1 if below[0, 2] == '#' else 0
                bug_count += 1 if below[0, 3] == '#' else 0
                bug_count += 1 if below[0, 4] == '#' else 0
            elif coordinate.x == 3 and coordinate.y == 2:
                bug_count += 1 if below[4, 0] == '#' else 0
                bug_count += 1 if below[4, 1] == '#' else 0
                bug_count += 1 if below[4, 2] == '#' else 0
                bug_count += 1 if below[4, 3] == '#' else 0
                bug_count += 1 if below[4, 4] == '#' else 0
            elif coordinate.x == 2 and coordinate.y == 3:
                bug_count += 1 if below[0, 4] == '#' else 0
                bug_count += 1 if below[1, 4] == '#' else 0
                bug_count += 1 if below[2, 4] == '#' else 0
                bug_count += 1 if below[3, 4] == '#' else 0
                bug_count += 1 if below[4, 4] == '#' else 0

        if above is not None:
            if coordinate.x == 0:
                bug_count += 1 if above[1, 2] == '#' else 0
            elif coordinate.x == 4:
                bug_count += 1 if above[3, 2] == '#' else 0

            if coordinate.y == 0:
                bug_count += 1 if above[2, 1] == '#' else 0
            elif coordinate.y == 4:
                bug_count += 1 if above[2, 3] == '#' else 0

        return bug_count



if __name__ == '__main__':
    code = Y2019D24("2019/24.txt")
    code.part1()
    code.part2()
