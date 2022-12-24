import itertools
from collections import Counter
from typing import Dict

from aoc.util.coordinate import Coordinate
from aoc.util.grid import InfiniteGrid
from aoc.util.inputs import Input


class Y2022D23(object):
    def __init__(self, file_name):
        input_grid = Input(file_name).grid()

        grid: InfiniteGrid[str] = InfiniteGrid[str]()
        for coordinate in input_grid.find('#'):
            grid[coordinate] = '#'
        # Now our grid is both infinite and only has '#' with no '.'

        self.round_10_empty_ground = 0
        self.first_round_no_elf_movement = 0
        for _round in itertools.count():
            existing_locations = set(grid.keys())
            grid = self._process_round(_round, grid)
            new_locations = set(grid.keys())
            if new_locations == existing_locations:
                print("No one moved!")
                self.first_round_no_elf_movement = _round + 1
                break

            if _round == 10:
                total_size = (grid.max_y - grid.min_y + 1) * (grid.max_x - grid.min_x + 1)
                self.round_10_empty_ground = total_size - len(new_locations)

    @staticmethod
    def _process_round(_round: int, grid: InfiniteGrid[str]) -> InfiniteGrid[str]:
        rule_start = _round % 4
        new_grid: InfiniteGrid[str] = InfiniteGrid[str]()

        proposals = Counter()
        elf_movement: Dict[Coordinate, Coordinate] = {}

        # First half of round, everyone makes proposals
        for elf in grid:
            n = elf.up()
            s = elf.down()
            w = elf.left()
            e = elf.right()
            nw = n.left()
            ne = n.right()
            sw = s.left()
            se = s.right()

            isolated = nw not in grid and n not in grid and ne not in grid and w not in grid and e not in grid and \
                       sw not in grid and s not in grid and se not in grid

            if isolated:
                elf_movement[elf] = elf  # We're not going anywhere, because we're all alone
                proposals[elf] = 1  # We're also the only people who can propose moving here, no one else will try
                continue  # Don't bother checking the rules

            rules = [
                n not in grid and nw not in grid and ne not in grid,
                s not in grid and sw not in grid and se not in grid,
                w not in grid and nw not in grid and sw not in grid,
                e not in grid and ne not in grid and se not in grid,
            ]

            movements = [n, s, w, e]  # Same order/index matching as the rules

            for rule_offset in range(4):
                rule_index = (rule_start + rule_offset) % 4
                if rules[rule_index]:
                    proposal = movements[rule_index]
                    proposals[proposal] += 1
                    elf_movement[elf] = proposal
                    break
            else:  # If we didn't break above, we didn't match any rule.
                elf_movement[elf] = elf  # We're not going anywhere, because we're blocked off
                proposals[elf] = 1  # We're also the only people who can propose moving here, no one else will try

        # Second half of round, everyone moves if they can
        for elf in grid:
            new_location = elf_movement[elf]
            if proposals[new_location] == 1:
                new_grid[new_location] = '#'  # We can move!
            else:
                new_grid[elf] = '#'  # Can't move, sorry

        # print(f'Round {_round + 1}')
        # new_grid.to_grid().print(not_found='.')
        # print()
        return new_grid

    def part1(self):
        result = self.round_10_empty_ground

        print("Part 1:", result)

    def part2(self):
        result = self.first_round_no_elf_movement

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D23("2022/23.txt")
    code.part1()
    code.part2()
