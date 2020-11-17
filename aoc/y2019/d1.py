from aoc.util.inputs import Input


class Y2019D1(object):
    def __init__(self, file_name):
        self.input = list(map(lambda x: int(x), Input(file_name).lines()))

    @staticmethod
    def _fuel_for_mass(mass):
        return (mass // 3) - 2

    def _fuel_for_mass_total(self, mass):
        fuel = self._fuel_for_mass(mass)
        total = 0

        while fuel > 0:
            total += fuel
            fuel = self._fuel_for_mass(fuel)

        return total

    def part1(self):
        fuel_needed = sum(map(lambda x: self._fuel_for_mass(x), self.input))

        print("Part 1:", fuel_needed)

    def part2(self):
        fuel_needed = sum(map(lambda x: self._fuel_for_mass_total(x), self.input))

        print("Part 2:", fuel_needed)


if __name__ == '__main__':
    code = Y2019D1("2019/1.txt")
    code.part1()
    code.part2()
