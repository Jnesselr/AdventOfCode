from itertools import product

from aoc.util.inputs import Input


class Y2017D4(object):
    def __init__(self, file_name):
        self.passphrases = Input(file_name).lines()

    def part1(self):
        result = 0

        for passphrase in self.passphrases:
            passphrase_list = passphrase.split(' ')
            passphrase_set = set(passphrase_list)
            if len(passphrase_list) == len(passphrase_set):
                result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        for passphrase in self.passphrases:
            passphrase_list = passphrase.split(' ')
            passphrase_set = set(passphrase_list)
            if len(passphrase_list) != len(passphrase_set):
                continue

            any_anagrams = any(
                True for a, b in product(passphrase_list, passphrase_list) if sorted(a) == sorted(b) and a != b
            )
            if not any_anagrams:
                result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D4("2017/4.txt")
    code.part1()
    code.part2()
