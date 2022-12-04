from aoc.util.inputs import Input


class Y2022D3(object):
    def __init__(self, file_name):
        self._rucksacks = Input(file_name).lines()

    @staticmethod
    def _get_score(character: str):
        if 'a' <= character <= 'z':
            return ord(character[0]) - ord('a') + 1
        elif 'A' <= character <= 'Z':
            return ord(character[0]) - ord('A') + 27
        else:
            raise ValueError()

    def part1(self):
        result = 0

        for rucksack in self._rucksacks:
            split = len(rucksack) // 2
            first, second = rucksack[:split], rucksack[split:]

            common = list(set(first).intersection(set(second)))[0]
            result += self._get_score(common)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for rucksack_id in range(0, len(self._rucksacks), 3):
            a, b, c = self._rucksacks[rucksack_id], self._rucksacks[rucksack_id + 1], self._rucksacks[rucksack_id + 2]
            common = list(set(a).intersection(set(b)).intersection(set(c)))[0]
            result += self._get_score(common)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D3("2022/3.txt")
    code.part1()
    code.part2()
