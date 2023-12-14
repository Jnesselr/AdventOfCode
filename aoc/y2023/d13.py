from dataclasses import dataclass

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


@dataclass(frozen=True)
class FlipResult:
    row_or_col: int
    differences: frozenset[Coordinate]

    @property
    def valid_flip_already(self):
        return len(self.differences) == 0

    @property
    def valid_flip_after_smudge(self):
        return len(self.differences) == 1


class Y2023D13(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        self.grids: list[Grid[str]] = []

        for group in groups:
            self.grids.append(Grid.from_str(group))

    def part1(self):
        result = 0

        for grid in self.grids:
            result += self._get_reflection_value(grid)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for grid in self.grids:
            result += self._get_reflection_value(grid, with_smudge=True)

        print("Part 2:", result)

    def _get_reflection_value(self, grid: Grid[str], with_smudge=False) -> int:
        results = []
        for row in range(grid.height - 1):
            row_result = self._is_reflecting_after_row(grid, row)
            results.append(row_result)
            if with_smudge and row_result.valid_flip_after_smudge:
                return 100 * (row + 1)
            elif not with_smudge and row_result.valid_flip_already:
                return 100 * (row + 1)

        for col in range(grid.width - 1):
            col_result = self._is_reflecting_after_col(grid, col)
            results.append(col_result)
            if with_smudge and col_result.valid_flip_after_smudge:
                return col + 1
            elif not with_smudge and col_result.valid_flip_already:
                return col + 1

        raise ValueError("Could not calculate grid reflection")

    @staticmethod
    def _is_reflecting_after_row(grid: Grid[str], row: int) -> FlipResult:
        num_rows_to_reflect = grid.width  # min(row + 1, grid.height - row)

        differences: set[Coordinate] = set()
        for i in range(num_rows_to_reflect):
            for x in range(grid.width):
                top = grid[x, row - i]
                bottom = grid[x, row + i + 1]
                if top is not None and bottom is not None and top != bottom:
                    differences.add(Coordinate(x, row - i, CoordinateSystem.X_RIGHT_Y_DOWN))

        return FlipResult(
            row_or_col=row,
            differences=frozenset(differences)
        )

    @staticmethod
    def _is_reflecting_after_col(grid: Grid[str], col: int) -> FlipResult:
        num_cols_to_reflect = grid.height  # max(col + 1, grid.height - col)

        differences: set[Coordinate] = set()
        for i in range(num_cols_to_reflect):
            for y in range(grid.height):
                left = grid[col - i, y]
                right = grid[col + i + 1, y]
                if left is not None and right is not None and left != right:
                    differences.add(Coordinate(col - i, y, CoordinateSystem.X_RIGHT_Y_DOWN))

        return FlipResult(
            row_or_col=col,
            differences=frozenset(differences)
        )


if __name__ == '__main__':
    code = Y2023D13("2023/13.txt")
    code.part1()
    code.part2()
