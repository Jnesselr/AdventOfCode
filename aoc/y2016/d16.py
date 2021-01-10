from aoc.util.inputs import Input


class Y2016D16(object):
    def __init__(self, file_name):
        self.start: str = Input(file_name).line()

    def _get_checksum(self, disk_size):
        data = self.start
        while len(data) < disk_size:
            data = data + "0" + data[::-1].replace('0', 'x').replace('1', '0').replace('x', '1')

        data = data[:disk_size]

        n = disk_size
        run_count = 0

        while n % 2 == 0:
            n //= 2
            run_count += 1

        run_length = 2**run_count

        checksum = ""
        for run_start in range(0, len(data), run_length):
            current = 1
            for index in range(run_length):
                current ^= int(data[run_start + index])

            checksum += str(current)
        return checksum

    def part1(self):
        result = self._get_checksum(272)

        print("Part 1:", result)

    def part2(self):
        result = self._get_checksum(35651584)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D16("2016/16.txt")
    code.part1()
    code.part2()
