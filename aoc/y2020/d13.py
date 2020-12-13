from aoc.util.chinese_remainder import ChineseRemainderTheorem
from aoc.util.inputs import Input


class Y2020D13(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.earliest_time = int(lines[0])

        self.buses = []
        for bus in lines[1].split(','):
            if bus != 'x':
                self.buses.append(int(bus))
            else:
                self.buses.append(bus)

    def part1(self):
        result = None

        test_time = self.earliest_time - 1
        actual_buses = list(filter(lambda x: x != 'x', self.buses))
        while result is None:
            test_time += 1
            for bus in actual_buses:
                if test_time % bus == 0:
                    result = bus

        result = result * (test_time - self.earliest_time)
        print("Part 1:", result)

    def part2(self):
        crt = ChineseRemainderTheorem()

        for time, bus in enumerate(self.buses):
            if bus == 'x':
                continue
            crt.a_mod_n(bus-time, bus)

        result = crt.result

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D13("2020/13.txt")
    code.part1()
    code.part2()
