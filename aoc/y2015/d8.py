from aoc.util.inputs import Input


class Y2015D8(object):
    def __init__(self, file_name):
        self.strings = Input(file_name).lines()

    def part1(self):
        result = 0

        for literal in self.strings:
            count = 0
            index = 1
            while index < len(literal) - 1:
                if literal[index] == '\\':
                    if literal[index + 1] == 'x':
                        index += 4
                    else:
                        index += 2
                else:
                    index += 1

                count += 1

            result += len(literal) - count

        print("Part 1:", result)

    def part2(self):
        result = 0

        for literal in self.strings:
            count = 2  # Start with the quotes on the ends
            index = 0
            while index < len(literal):
                if literal[index] == '\\':
                    count += 2
                elif literal[index] == '"':
                    count += 2
                else:
                    count += 1
                index += 1

            result += count - len(literal)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D8("2015/8.txt")
    code.part1()
    code.part2()
