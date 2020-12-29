from itertools import product
from math import sqrt
from time import sleep
from typing import List, Union

from aoc.util.grid import Grid
from aoc.util.inputs import Input


class FractalArt(object):
    def __init__(self, rules: List[str]):
        self._rules = {}

        for rule in rules:
            _in, _out = rule.split(' => ')
            _in_grid = self._to_grid(_in)
            _out_grid = self._to_grid(_out)

            out_str = self._to_str(_out_grid)

            _in_grids = [
                _in_grid,
                _in_grid.rotate_right(),
                _in_grid.rotate_right().rotate_right(),
                _in_grid.rotate_right().rotate_right().rotate_right(),
                _in_grid.flip_vertical(),
                _in_grid.flip_vertical().rotate_right(),
                _in_grid.flip_horizontal(),
                _in_grid.flip_horizontal().rotate_right(),
            ]

            for grid in _in_grids:
                in_str = self._to_str(grid)
                if in_str in self._rules:
                    continue

                self._rules[in_str] = out_str

        self.art = [".#...####"]

    @property
    def num_on(self):
        return sum(1 for art in self.art for x in art if x == '#')

    def step(self):
        tile_size = int(sqrt(len(self.art[0])))
        input_size = int(sqrt(len(self.art)))

        if tile_size == 2:
            art_output_size = 3 * input_size
            self.art = [self._rules[x] for x in self.art]

            if art_output_size % 2 == 0:
                output_size = art_output_size // 2
                output = [""] * (output_size * output_size)

                for row, col in product(range(art_output_size), repeat=2):
                    input_str_index = input_size * (row // 3) + (col // 3)
                    input_str = self.art[input_str_index]
                    index_in_input_str = 3 * (row % 3) + (col % 3)

                    output_index = output_size * (row // 2) + (col // 2)
                    output[output_index] += input_str[index_in_input_str]

                self.art = output

        elif tile_size == 3:
            output_size = 2 * input_size
            output = [""] * (output_size * output_size)

            for row, col in product(range(input_size), repeat=2):
                input_index = input_size * row + col
                in_tile = self.art[input_index]
                out_tile = self._rules[in_tile]
                for i, j in product(range(2), repeat=2):
                    tile_index = 2 * i + j
                    output_index = output_size * (2 * row + i) + (2 * col + j)
                    output[output_index] = out_tile[tile_index]

            self.art = output
        else:
            raise ValueError(f"Input size not understood: {tile_size}")

    @staticmethod
    def _to_str(grid: Grid[str]) -> Union[str, List[str]]:
        if grid.width <= 3:
            result = ""
            for row, col in product(range(grid.width), repeat=2):
                result += grid[col, row]

            return result

        result = []
        for row, col in product(range(0, grid.width, 2), repeat=2):
            result_str = ""
            for i, j in product(range(2), repeat=2):
                result_str += grid[col + j, row + i]
            result.append(result_str)

        return result

    @staticmethod
    def _to_grid(rule: str) -> Grid[str]:
        rows = rule.split('/')
        grid = Grid[str](len(rows), len(rows))

        for row_i in range(len(rows)):
            for col_i in range(len(rows)):
                grid[col_i, row_i] = rows[row_i][col_i]

        return grid


class Y2017D21(object):
    def __init__(self, file_name):
        rules = Input(file_name).lines()
        fractal_art = FractalArt(rules)

        self.count_at_5 = 0
        self.count_at_18 = 0

        for i in range(18):
            fractal_art.step()

            if i == 4:
                self.count_at_5 = fractal_art.num_on
            if i == 17:
                self.count_at_18 = fractal_art.num_on

    def part1(self):
        result = self.count_at_5

        print("Part 1:", result)

    def part2(self):
        result = self.count_at_18

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D21("2017/21.txt")
    code.part1()
    code.part2()
