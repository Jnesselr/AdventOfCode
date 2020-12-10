from aoc.util.inputs import Input


class Y2020D10(object):
    def __init__(self, file_name):
        self.adapters = sorted([int(x) for x in Input(file_name).lines()])
        self.device_jolts = max(self.adapters) + 3

    def part1(self):
        differences = {
            self.adapters[0]: 1,  # Lowest adapter to outlet
            3: 1,  # Highest adapter to my device
        }

        for i in range(len(self.adapters) - 1):
            difference = (self.adapters[i + 1] - self.adapters[i])
            differences[difference] = differences.setdefault(difference, 0) + 1

        result = differences[1] * differences[3]

        print("Part 1:", result)

    def part2(self):
        # Use dynamic programming to figure out possibilities starting from outlet
        possibility_map = {
            0: 1
        }

        for adapter in self.adapters:
            total = 0
            for lower_adapter in range(adapter - 3, adapter):
                if lower_adapter not in possibility_map:
                    continue

                total += possibility_map[lower_adapter]

            possibility_map[adapter] = total

        result = possibility_map[self.device_jolts - 3]

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D10("2020/10.txt")
    code.part1()
    code.part2()
