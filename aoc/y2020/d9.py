from aoc.util.inputs import Input


class Y2020D9(object):
    def __init__(self, file_name):
        self.input = [int(x) for x in Input(file_name).lines()]
        preamble = 25

        for i in range(preamble, len(self.input)):
            number = self.input[i]
            previous_numbers = set(self.input[i-preamble:i])
            test = previous_numbers.intersection(number - x for x in previous_numbers)

            if len(test) <= 1:
                self.bad_number = number
                break

    def part1(self):
        result = self.bad_number

        print("Part 1:", result)

    def part2(self):
        current_sum = self.input[0]
        start = 0
        end = 0

        while current_sum != self.bad_number:
            while current_sum < self.bad_number:
                end += 1
                current_sum += self.input[end]

            while current_sum > self.bad_number:
                current_sum -= self.input[start]
                start += 1

        new_range = self.input[start:end]

        result = min(new_range) + max(new_range)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D9("2020/9.txt")
    code.part1()
    code.part2()
