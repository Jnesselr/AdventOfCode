from aoc.util.intcode import Intcode


class Y2019D7(object):
    def __init__(self, file_name):
        self.comp_a = Intcode(file_name)
        self.comp_b = Intcode(file_name)
        self.comp_c = Intcode(file_name)
        self.comp_d = Intcode(file_name)
        self.comp_e = Intcode(file_name)

    @staticmethod
    def _iterator(start, end):
        for a in range(start, end + 1):
            for b in range(start, end + 1):
                for c in range(start, end + 1):
                    for d in range(start, end + 1):
                        for e in range(start, end + 1):
                            if len({a, b, c, d, e}) == 5:
                                yield [a, b, c, d, e]

    def _reset_and_start_computers(self):
        self.comp_a.reset()
        self.comp_a.run()
        self.comp_b.reset()
        self.comp_b.run()
        self.comp_c.reset()
        self.comp_c.run()
        self.comp_d.reset()
        self.comp_d.run()
        self.comp_e.reset()
        self.comp_e.run()

    def part1(self):
        result = 0

        for settings in self._iterator(0, 4):
            self._reset_and_start_computers()

            self.comp_a.input(settings[0])
            self.comp_b.input(settings[1])
            self.comp_c.input(settings[2])
            self.comp_d.input(settings[3])
            self.comp_e.input(settings[4])

            self.comp_a.input(0)
            self.comp_b.input(self.comp_a.output())
            self.comp_c.input(self.comp_b.output())
            self.comp_d.input(self.comp_c.output())
            self.comp_e.input(self.comp_d.output())

            result = max(result, self.comp_e.output())

        print("Part 1:", result)

    def part2(self):
        result = 0

        for settings in self._iterator(5, 9):
            self._reset_and_start_computers()

            self.comp_a.input(settings[0])
            self.comp_b.input(settings[1])
            self.comp_c.input(settings[2])
            self.comp_d.input(settings[3])
            self.comp_e.input(settings[4])

            self.comp_a.input(0)

            while not self.comp_a.halted:
                self.comp_b.input(self.comp_a.output())
                self.comp_c.input(self.comp_b.output())
                self.comp_d.input(self.comp_c.output())
                self.comp_e.input(self.comp_d.output())

                if not self.comp_a.halted:
                    self.comp_a.input(self.comp_e.output())

            result = max(result, self.comp_e.output())

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D7("2019/7.txt")
    code.part1()
    code.part2()
