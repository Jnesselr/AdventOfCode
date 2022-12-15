import re

from z3 import Solver, Ints, Abs

from aoc.util.inputs import Input


class Y2022D15(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.mapping = {}

        line_regex = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

        self.min_x = 1e24
        self.max_x = -1e24
        self.min_y = 1e24
        self.max_y = -1e24

        for line in lines:
            match = line_regex.match(line)
            s_x, s_y, b_x, b_y = match.groups()
            s_x = int(s_x)
            s_y = int(s_y)
            b_x = int(b_x)
            b_y = int(b_y)

            self.mapping[s_x, s_y] = (b_x, b_y)

    def part1(self):
        invalid_row = set()
        row = 2000000
        for sensor, beacon in self.mapping.items():
            manhattan = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])
            # print(sensor, beacon, manhattan)

            diff_y = abs(sensor[1] - row)
            if diff_y > manhattan:
                continue

            for diff_x in range(-manhattan + diff_y, manhattan - diff_y):
                invalid_row.add(sensor[0] + diff_x)
        result = len(invalid_row)

        print("Part 1:", result)

    def part2(self):
        solver = Solver()

        distress_x, distress_y = Ints('distress_x distress_y')
        solver.add(distress_x >= 0)
        solver.add(distress_y <= 4000000)

        min_x = 1e24
        max_x = -1e24
        min_y = 1e24
        max_y = -1e24

        for sensor, beacon in self.mapping.items():
            manhattan = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

            solver.add(Abs(distress_x - sensor[0]) + Abs(distress_y - sensor[1]) > manhattan)
            min_x = min(min_x, sensor[0])
            max_x = max(max_x, sensor[0])
            min_y = min(min_y, sensor[1])
            max_y = max(max_y, sensor[1])

        solver.add(distress_x >= min_x)
        solver.add(distress_x <= max_x)
        solver.add(distress_y >= min_x)
        solver.add(distress_y <= max_y)

        solver.check()
        model = solver.model()

        result = model[distress_x].as_long() * 4000000 + model[distress_y].as_long()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D15("2022/15.txt")
    code.part1()
    code.part2()
