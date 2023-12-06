from aoc.util.inputs import Input


class Y2023D6(object):
    def __init__(self, file_name):
        time_line, distance_line = Input(file_name).lines()
        self.times = self._get_ints(time_line)
        self.distances = self._get_ints(distance_line)

    @staticmethod
    def _get_ints(line: str):
        first_space_index = line.index(' ')
        line = line[first_space_index:].strip()
        while '  ' in line:
            line = line.replace('  ', ' ')

        return [int(x) for x in line.split(' ')]

    def part1(self):
        result = self._race(self.times, self.distances)

        print("Part 1:", result)

    def part2(self):
        times = [int(''.join(str(x) for x in self.times))]
        distances = [int(''.join(str(x) for x in self.distances))]

        result = self._race(times, distances)

        print("Part 2:", result)

    @staticmethod
    def _race(times, distances):
        result = 1
        for time, best_distance in zip(times, distances):
            ways_to_win = 0
            for hold_time in range(0, time + 1):
                distance = (time - hold_time) * hold_time
                if distance > best_distance:
                    ways_to_win += 1

            result *= ways_to_win
        return result


if __name__ == '__main__':
    code = Y2023D6("2023/6.txt")
    code.part1()
    code.part2()
