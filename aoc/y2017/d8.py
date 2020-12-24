import re

from aoc.util.inputs import Input


class CPU(object):
    def __init__(self, lines):
        self.registers = {}
        self.largest_register_ever = 0

        for line in lines:
            matched = re.match(r'(\w+) (dec|inc) (-?\d+) if (\w+) (>|<|>=|<=|==|!=) (-?\d+)', line)

            change_register = matched.group(1)
            change_type = matched.group(2)
            change_value = int(matched.group(3))
            test_register = matched.group(4)
            test_type = matched.group(5)
            test_value = int(matched.group(6))
            change_register_value = self.registers.setdefault(change_register, 0)
            test_register_value = self.registers.setdefault(test_register, 0)

            should_process = (test_type == '>' and test_register_value > test_value) or \
                             (test_type == '<' and test_register_value < test_value) or \
                             (test_type == '>=' and test_register_value >= test_value) or \
                             (test_type == '<=' and test_register_value <= test_value) or \
                             (test_type == '==' and test_register_value == test_value) or \
                             (test_type == '!=' and test_register_value != test_value)

            if should_process:
                if change_type == 'inc':
                    new_value = change_register_value + change_value
                else:
                    new_value = change_register_value - change_value

                self.registers[change_register] = new_value
                self.largest_register_ever = max(self.largest_register_ever, new_value)

    @property
    def largest_register(self):
        if len(self.registers) == 0:
            return 0
        return max(self.registers.values())


class Y2017D8(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.cpu = CPU(lines)

    def part1(self):
        result = self.cpu.largest_register

        print("Part 1:", result)

    def part2(self):
        result = self.cpu.largest_register_ever

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D8("2017/8.txt")
    code.part1()
    code.part2()
