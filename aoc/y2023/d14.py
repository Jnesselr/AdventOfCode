from typing import Callable

from aoc.util.coordinate import Coordinate, TurtleDirection
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2023D14(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()
        self.round_rocks: frozenset[Coordinate] = frozenset(self.grid.find('O'))
        self.square_rocks: frozenset[Coordinate] = frozenset(self.grid.find('#'))

    def part1(self):
        round_rocks = frozenset(self._roll(set(self.round_rocks), TurtleDirection.NORTH))

        result = self._calculate_load(round_rocks)

        print("Part 1:", result)

    def part2(self):
        round_rocks = set(self.round_rocks)

        index = 1
        seen: dict[frozenset[Coordinate], int] = {}
        load: dict[int, int] = {}
        while True:
            round_rocks = self._roll(round_rocks, TurtleDirection.NORTH)
            round_rocks = self._roll(round_rocks, TurtleDirection.WEST)
            round_rocks = self._roll(round_rocks, TurtleDirection.SOUTH)
            round_rocks = self._roll(round_rocks, TurtleDirection.EAST)

            round_rocks = frozenset(round_rocks)
            load[index] = self._calculate_load(round_rocks)

            if round_rocks in seen:
                lower = seen[round_rocks]
                diff = index - lower
                fetch_index = (1000000000 - lower) % diff + lower
                result = load[fetch_index]
                break

            seen[round_rocks] = index

            index += 1

        print("Part 2:", result)

    def _roll(self,
              round_rock_set: set[Coordinate],
              direction: TurtleDirection) -> set[Coordinate]:
        round_rocks: list[Coordinate] = list(round_rock_set)

        if direction == TurtleDirection.NORTH:
            round_rocks = sorted(round_rocks, key=lambda c: c.y)
        elif direction == TurtleDirection.SOUTH:
            round_rocks = sorted(round_rocks, key=lambda c: -c.y)
        elif direction == TurtleDirection.WEST:
            round_rocks = sorted(round_rocks, key=lambda c: c.x)
        elif direction == TurtleDirection.EAST:
            round_rocks = sorted(round_rocks, key=lambda c: -c.x)

        new_rock_set: set[Coordinate] = set()

        for rock in round_rocks:
            keep_going = True
            while keep_going:
                if direction == TurtleDirection.NORTH:
                    next_location = rock.up()
                elif direction == TurtleDirection.SOUTH:
                    next_location = rock.down()
                elif direction == TurtleDirection.WEST:
                    next_location = rock.left()
                elif direction == TurtleDirection.EAST:
                    next_location = rock.right()
                else:
                    raise ValueError()

                keep_going = True
                if next_location.x < 0 or next_location.x >= self.grid.width:
                    keep_going = False
                if next_location.y < 0 or next_location.y >= self.grid.height:
                    keep_going = False

                if next_location in self.square_rocks or next_location in new_rock_set:
                    keep_going = False

                if keep_going:
                    rock = next_location

            new_rock_set.add(rock)

        return new_rock_set

    def _calculate_load(self, round_rock_set: frozenset[Coordinate]):
        return sum([self.grid.height - c.y for c in round_rock_set])


if __name__ == '__main__':
    code = Y2023D14("2023/14.txt")
    code.part1()
    code.part2()
