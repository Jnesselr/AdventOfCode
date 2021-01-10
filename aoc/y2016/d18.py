from aoc.util.inputs import Input


class Y2016D18(object):
    def __init__(self, file_name):
        self.starting_row = Input(file_name).line()

    def part1(self):
        result = 0

        gen = self._tile_generator()
        for _ in range(40):
            result += next(gen).count('.')

        print("Part 1:", result)

    def part2(self):
        result = 0

        gen = self._tile_generator()
        for _ in range(400000):
            result += next(gen).count('.')

        print("Part 2:", result)

    def _tile_generator(self):
        row = self.starting_row

        while True:
            yield row

            new_row = ""

            for i in range(len(row)):
                left_is_trap = row[i-1] == '^' if i > 0 else False
                center_is_trap = row[i] == '^'
                right_is_trap = row[i+1] == '^' if i < len(row)-1 else False

                if left_is_trap and center_is_trap and not right_is_trap:
                    new_row += '^'
                elif not left_is_trap and center_is_trap and right_is_trap:
                    new_row += '^'
                elif left_is_trap and not center_is_trap and not right_is_trap:
                    new_row += '^'
                elif not left_is_trap and not center_is_trap and right_is_trap:
                    new_row += '^'
                else:
                    new_row += '.'

            row = new_row


if __name__ == '__main__':
    code = Y2016D18("2016/18.txt")
    code.part1()
    code.part2()
