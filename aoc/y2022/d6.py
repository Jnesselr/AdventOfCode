from aoc.util.inputs import Input


class Y2022D6(object):
    def __init__(self, file_name):
        self.packet = Input(file_name).line()

    def _get_start_of(self, window_size: int):
        for i in range(len(self.packet) - window_size + 1):
            if len(set(self.packet[i: i + window_size])) == window_size:
                return i + window_size

    def part1(self):
        result = self._get_start_of(4)  # Packet

        print("Part 1:", result)

    def part2(self):
        result = self._get_start_of(14)  # Message

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D6("2022/6.txt")
    code.part1()
    code.part2()
