from aoc.util.inputs import Input


class Y2017D1(object):
    def __init__(self, file_name):
        self.input = Input(file_name).line()

    def part1(self):
        result = 0
        input_length = len(self.input)

        for i in range(input_length):
            current_digit = int(self.input[i])
            next_digit = int(self.input[(i+1) % input_length])

            if current_digit == next_digit:
                result += current_digit

        print("Part 1:", result)

    def part2(self):
        result = 0
        input_length = len(self.input)

        for i in range(input_length):
            current_digit = int(self.input[i])
            next_i = (i + (input_length // 2)) % input_length
            next_digit = int(self.input[next_i])

            if current_digit == next_digit:
                result += current_digit

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D1("2017/1.txt")
    code.part1()
    code.part2()
