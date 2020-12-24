from aoc.util.inputs import Input


class Y2017D5(object):
    def __init__(self, file_name):
        self.input = Input(file_name).ints()

    def part1(self):
        result = 0

        cpu_instructions = self.input.copy()
        input_length = len(self.input)
        pointer = 0

        while 0 <= pointer < input_length:
            value = cpu_instructions[pointer]
            cpu_instructions[pointer] += 1
            pointer += value
            result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        cpu_instructions = self.input.copy()
        input_length = len(self.input)
        pointer = 0

        while 0 <= pointer < input_length:
            value = cpu_instructions[pointer]
            if value >= 3:
                cpu_instructions[pointer] -= 1
            else:
                cpu_instructions[pointer] += 1
            pointer += value
            result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D5("2017/5.txt")
    code.part1()
    code.part2()
