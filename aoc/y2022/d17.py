import string

from tqdm.auto import tqdm

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.cycle_finder import CycleFinder
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2022D17(object):
    def __init__(self, file_name):
        self.instructions = Input(file_name).line()

        # All rocks are made so 0, 0 is the bottom left corner

        horizontal_line = [
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(2, 0),
            Coordinate(3, 0),
        ]

        plus = [
            Coordinate(1, 0),
            Coordinate(0, 1),
            Coordinate(1, 1),
            Coordinate(2, 1),
            Coordinate(1, 2),
        ]

        backwards_l = [
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(2, 0),
            Coordinate(2, 1),
            Coordinate(2, 2),
        ]

        vertical_line = [
            Coordinate(0, 0),
            Coordinate(0, 1),
            Coordinate(0, 2),
            Coordinate(0, 3),
        ]

        square = [
            Coordinate(0, 0),
            Coordinate(0, 1),
            Coordinate(1, 0),
            Coordinate(1, 1),
        ]

        self.rocks = [
            horizontal_line,
            plus,
            backwards_l,
            vertical_line,
            square
        ]

    def _drop_rocks(self, rocks_to_place: int) -> int:
        rock_index = -1
        instruction_index = -1

        grid: InfiniteGrid[str] = InfiniteGrid[str]()
        cycle_finder = CycleFinder(needs_repeated=2)
        height_at_index = {}

        for column in range(7):
            grid[Coordinate(column, -1)] = '-'

        highest_row = 0

        for i in range(rocks_to_place):
            rock_index = (rock_index + 1) % len(
                self.rocks)  # Yes, I could just modulo _ but I like the symmetry to instructions

            starting_rock = self.rocks[rock_index]
            lower_left_coordinate = Coordinate(2, highest_row + 3)
            rock = starting_rock = [c + lower_left_coordinate for c in starting_rock]

            settled = False
            while not settled:
                instruction_index = (instruction_index + 1) % len(self.instructions)

                if '>' == self.instructions[instruction_index]:
                    new_rock = [c.right() for c in rock]
                elif '<' == self.instructions[instruction_index]:
                    new_rock = [c.left() for c in rock]
                else:
                    raise ValueError()

                # If it's not all in range of our chamber, or collides with another rock, we can't move
                if not all(0 <= c.x <= 6 for c in new_rock) or any(c in grid for c in new_rock):
                    new_rock = rock

                # We've collided with something. Use < instead of <= here because we've moved down since calculating rock_by_column
                down_rock = [c.down() for c in new_rock]
                if any(c in grid for c in down_rock):
                    rock = new_rock
                    settled = True
                else:
                    rock = down_rock  # rock for next iteration

            for c in rock:
                grid[c] = string.ascii_uppercase[i % 26]

            rock_height = [1, 3, 3, 4, 2][rock_index]
            height_fell = starting_rock[0].y - rock[0].y - 3
            # print(starting_rock, '    ', rock, height_fell)

            change_in_height = rock_height - height_fell if rock_height >= height_fell else 0

            cycle_finder[i] = (rock_index, height_fell)
            # print(i, rock_index, height_fell, grid.max_y, change_in_height, cycle_finder.cycle_found)

            height_at_index[i] = grid.max_y
            highest_row = height_at_index[i] + 1

            if cycle_finder.cycle_found:
                break

        if not cycle_finder.cycle_found:
            return grid.max_y - grid.min_y

        # print(cycle_finder.cycle_start)
        # print(cycle_finder.cycle_size)

        end_height = height_at_index[cycle_finder.cycle_start + cycle_finder.cycle_size]
        cycle_height = end_height - height_at_index[cycle_finder.cycle_start]
        start_height = height_at_index[cycle_finder.cycle_start - 1]
        whole_cycles = (rocks_to_place - cycle_finder.cycle_start) // cycle_finder.cycle_size

        total_height = start_height + whole_cycles * cycle_height
        more_cycles_needed = rocks_to_place - (whole_cycles * cycle_finder.cycle_size) - cycle_finder.cycle_start
        more_height_needed = height_at_index[cycle_finder.cycle_start + more_cycles_needed] - height_at_index[
            cycle_finder.cycle_start]  # Since we probably don't end on a cycle

        # print(
        #     start_height,
        #     cycle_finder.cycle_size,
        #     cycle_height,
        #     whole_cycles,
        #     total_height,
        #     more_cycles_needed,
        #     more_height_needed
        # )

        total_height += more_height_needed

        return total_height

    def part1(self):
        # TODO This code does not seem to work for the example in part 1. I get 3069 instead of 3068.
        result = self._drop_rocks(2022)

        print("Part 1:", result)

    def part2(self):
        result = self._drop_rocks(1000000000000)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D17("2022/17.txt")
    code.part1()
    code.part2()
