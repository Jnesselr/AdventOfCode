from aoc.util.inputs import Input


class Y2015D1(object):
    def __init__(self, file_name):
        floors = Input(file_name).line()

        self.floor = 0
        self.first_basement_index = None
        for index, character in enumerate(floors):
            self.floor += 1 if character == '(' else -1
            if self.floor == -1 and self.first_basement_index is None:
                self.first_basement_index = index + 1

    def part1(self):
        result = self.floor

        print("Part 1:", result)

    def part2(self):
        result = self.first_basement_index

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D1("2015/1.txt")
    code.part1()
    code.part2()
