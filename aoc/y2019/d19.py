from aoc.util.grid import Grid
from aoc.util.inputs import Input
from aoc.util.intcode import Intcode
from aoc.util.search import BinarySearch


class Y2019D19(object):
    def __init__(self, file_name):
        self.drone = Intcode(file_name)

    def _is_beam(self, x: int, y: int):
        if x < 0 or y < 0:
            return False

        self.drone.reset()
        self.drone.run()
        self.drone.input(x)
        self.drone.input(y)
        return self.drone.output() == 1

    def part1(self):
        result = 0
        for x in range(50):
            for y in range(50):
                if self._is_beam(x, y):
                    result += 1

        print("Part 1:", result)

    def part2(self):
        square_side = 100
        end_cache = {}

        def valid_y(y):
            # Bit of a hack, but the beam isn't continuous
            if y < 10:
                return False

            if y in end_cache:
                end_x = end_cache[y]
            else:
                start_search = BinarySearch(lambda x: self._is_beam(x, y))
                start_x = start_search.earliest(0, lambda x: x+1)
                end_x = start_search.latest(start_x, lambda x: x*2)
                end_cache[y] = end_x

            test_x = end_x - square_side + 1
            test_y = y + square_side - 1
            beam = self._is_beam(test_x, test_y)
            return beam

        search = BinarySearch(valid_y)
        found_y = search.earliest(1, lambda x: x * 2)
        found_x = end_cache[found_y] - square_side + 1
        result = found_x * 10000 + found_y

        print("Part 2:", result)

    def _find_beam_right(self, start_x: int, y: int, max_search_x=10000):
        seen_beam = False
        for x in range(start_x, max_search_x):
            is_beam = self._is_beam(x, y)
            if not is_beam and seen_beam:
                return x-1

            if is_beam:
                seen_beam = True
        return None


if __name__ == '__main__':
    code = Y2019D19("2019/19.txt")
    code.part1()
    code.part2()
