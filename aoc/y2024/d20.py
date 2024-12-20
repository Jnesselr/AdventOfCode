from aoc.util.inputs import Input


class Y2024D20(object):
    def __init__(self, file_name):
        grid = Input(file_name).grid()
        start = grid.find('S')[0]
        end = grid.find('E')[0]
        grid[start] = '.'
        grid[end] = '.'

        self._racetrack = grid.find_path(start, end, '.')

    def part1(self):
        result = self._get_total_shortcuts(2, 100)

        print("Part 1:", result)

    def part2(self):
        result = self._get_total_shortcuts(20, 100)

        print("Part 2:", result)

    def _get_total_shortcuts(self, picosecond_jump: int, time_savings_needed: int) -> int:
        result = 0

        for before_i in range(0, len(self._racetrack) - time_savings_needed - 2):
            for after_i in range(before_i + time_savings_needed + 2, len(self._racetrack)):
                before = self._racetrack[before_i]
                after = self._racetrack[after_i]

                manhattan = before.manhattan(after)
                if manhattan > picosecond_jump:
                    continue  # We cannot make this jump in time

                time_saved = after_i - before_i - manhattan

                if time_saved < time_savings_needed:
                    continue  # We didn't save enough time after all

                result += 1

        return result


if __name__ == '__main__':
    code = Y2024D20("2024/20.txt")
    code.part1()
    code.part2()
