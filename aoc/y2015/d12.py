import json

from aoc.util.inputs import Input


class Y2015D12(object):
    def __init__(self, file_name):
        self.document = json.loads(Input(file_name).line())

    def part1(self):
        result = self._get_my_sum(self.document)

        print("Part 1:", result)

    def part2(self):
        result = self._get_my_sum(self.document, True)

        print("Part 2:", result)

    @classmethod
    def _get_my_sum(cls, document, ignore_red=False):
        if isinstance(document, int):
            return document
        elif isinstance(document, str):
            return 0
        elif isinstance(document, list):
            return sum(cls._get_my_sum(x, ignore_red) for x in document)
        elif isinstance(document, dict):
            values = document.values()
            if "red" in values and ignore_red:
                return 0
            return sum(cls._get_my_sum(x, ignore_red) for x in values)


if __name__ == '__main__':
    code = Y2015D12("2015/12.txt")
    code.part1()
    code.part2()
