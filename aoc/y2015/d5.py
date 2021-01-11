from collections import Counter

from aoc.util.inputs import Input


class Y2015D5(object):
    def __init__(self, file_name):
        self.strings = Input(file_name).lines()

    def part1(self):
        result = 0

        for string in self.strings:
            result += 1 if self._nice_part1(string) else 0

        print("Part 1:", result)

    def part2(self):
        result = 0

        for string in self.strings:
            result += 1 if self._nice_part2(string) else 0

        print("Part 2:", result)

    @staticmethod
    def _nice_part1(string):
        bad_strings = ["ab", "cd", "pq", "xy"]
        for bad in bad_strings:
            if bad in string:
                return False

        vowels = "aeiou"
        common = dict(Counter(string).most_common())
        vowel_count = sum(common.setdefault(vowel, 0) for vowel in vowels)
        if vowel_count < 3:
            return False

        for index in range(len(string)-1):
            if string[index] == string[index+1]:
                return True

        return False

    @staticmethod
    def _nice_part2(string):
        two_letters_twice = False

        for x in range(len(string)-1):
            for y in range(x+2, len(string)-1):
                if string[x] == string[y] and string[x+1] == string[y+1]:
                    two_letters_twice = True

        repeat_one_between = False
        for x in range(len(string)-2):
            if string[x] == string[x+2]:
                repeat_one_between = True

        return two_letters_twice and repeat_one_between


if __name__ == '__main__':
    code = Y2015D5("2015/5.txt")
    code.part1()
    code.part2()
