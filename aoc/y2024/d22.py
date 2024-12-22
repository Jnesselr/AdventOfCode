import functools
from collections import Counter

from aoc.util.inputs import Input


class Y2024D22(object):
    def __init__(self, file_name):
        self._buyers = Input(file_name).ints()

    def part1(self):
        result = 0

        for buyer in self._buyers:
            secret = buyer
            for _ in range(2000):
                next_secret = self._next_secret_number(secret)
                secret = next_secret
            result += secret

        print("Part 1:", result)

    def part2(self):
        buyer_total_best = Counter()

        for buyer in self._buyers:
            seen_differences = set()
            secret = buyer
            t = (0, 0, 0, 0)
            for i in range(2000):
                next_secret = self._next_secret_number(secret)

                t = (t[1], t[2], t[3], (next_secret % 10) - (secret % 10))
                secret = next_secret

                if i >= 3 and t not in seen_differences:
                    seen_differences.add(t)
                    buyer_total_best[t] += secret % 10

        most_common = buyer_total_best.most_common(1)[0]
        result = most_common[1]

        print("Part 2:", result)

    @staticmethod
    @functools.cache
    def _next_secret_number(number: int) -> int:
        mod_value = 16777216
        result = number * 64
        number ^= result
        number %= mod_value
        result = number // 32
        number ^= result
        number %= mod_value
        result = number * 2048
        number ^= result
        number %= mod_value

        return number


if __name__ == '__main__':
    code = Y2024D22("2024/22.txt")
    code.part1()
    code.part2()
