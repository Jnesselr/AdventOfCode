import hashlib
import itertools

from aoc.util.inputs import Input


class Y2015D4(object):
    def __init__(self, file_name):
        self.secret_key = Input(file_name).line()

        self.five_leading_zeros = None
        self.six_leading_zeros = None
        for number in itertools.count(1):
            md5_hex = hashlib.md5(f'{self.secret_key}{number}'.encode()).hexdigest()
            if md5_hex.startswith("00000") and self.five_leading_zeros is None:
                self.five_leading_zeros = number
            if md5_hex.startswith("000000") and self.six_leading_zeros is None:
                self.six_leading_zeros = number

            if self.five_leading_zeros is not None and self.six_leading_zeros is not None:
                break

    def part1(self):
        result = self.five_leading_zeros

        print("Part 1:", result)

    def part2(self):
        result = self.six_leading_zeros

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2015D4("2015/4.txt")
    code.part1()
    code.part2()
