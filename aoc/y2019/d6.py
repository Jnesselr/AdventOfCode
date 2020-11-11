from aoc.util.inputs import Input


class Y2019D6(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.orbits = {}

        for line in lines:
            split = line.split(')')
            self.orbits[split[1].strip()] = split[0].strip()

    def _orbit_chain(self, start):
        result = [start]
        current = start

        while current != 'COM':
            current = self.orbits[current]
            result.append(current)

        result.reverse()
        return result

    def part1(self):
        result = 0
        for obj in self.orbits.keys():
            result += len(self._orbit_chain(obj)) - 1

        print("Part 1:", result)

    def part2(self):
        you = self._orbit_chain('YOU')
        san = self._orbit_chain('SAN')

        index = 0
        for index in range(min(len(you), len(san))):
            if you[index] != san[index]:
                break

        result = len(you[index:]) + len(san[index:]) - 2

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2019D6("2019/6.txt")
    code.part1()
    code.part2()
