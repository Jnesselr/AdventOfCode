from aoc.util.inputs import Input


class Y2024D2(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self._reports: list[list[int]] = []
        for line in lines:
            self._reports.append([int(x) for x in line.split(' ')])

    def part1(self):
        result = 0

        for report in self._reports:
            if self._is_report_safe(report):
                result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        for report in self._reports:
            any_safe = self._is_report_safe(report)
            for slice_index in range(len(report)):
                new_report = report[:slice_index] + report[slice_index+1:]
                if self._is_report_safe(new_report):
                    any_safe = True

            if any_safe:
                result += 1

        print("Part 2:", result)

    @staticmethod
    def _is_report_safe(report: list[int]) -> bool:
        increasing = (report[1] - report[0]) > 0
        for i in range(len(report) - 1):
            if not (1 <= abs(report[i + 1] - report[i]) <= 3):
                return False
            if increasing and report[i + 1] < report[i]:
                return False
            if not increasing and report[i + 1] > report[i]:
                return False

        return True


if __name__ == '__main__':
    code = Y2024D2("2024/2.txt")
    code.part1()
    code.part2()
