from aoc.util.inputs import Input


class Y2023D9(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.measurements: list[list[int]] = []
        for line in lines:
            self.measurements.append([int(x) for x in line.split(' ')])

    def part1(self):
        result = 0

        for measurement in self.measurements:
            result += self._find_next_measurement(measurement, backwards=False)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for measurement in self.measurements:
            result += self._find_next_measurement(measurement, backwards=True)

        print("Part 2:", result)

    def _find_next_measurement(self, measurement: list[int], backwards: bool) -> int:
        all_are_zeros = all([x == 0 for x in measurement])

        if all_are_zeros:
            return 0
        else:
            new_measurement = [measurement[t + 1] - measurement[t] for t in range(len(measurement) - 1)]

            if backwards:
                return measurement[0] - self._find_next_measurement(new_measurement, backwards)
            else:
                return measurement[-1] + self._find_next_measurement(new_measurement, backwards)


if __name__ == '__main__':
    code = Y2023D9("2023/9.txt")
    code.part1()
    code.part2()
