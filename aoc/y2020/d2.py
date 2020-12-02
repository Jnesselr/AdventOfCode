import re
from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass
class Password(object):
    min: int
    max: int
    letter: str
    password: str


class Y2020D2(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.passwords = []
        for line in lines:
            matched = re.match(r"(\d+)-(\d+) (\w): (\w+)", line)
            self.passwords.append(Password(
                min=int(matched.group(1)),
                max=int(matched.group(2)),
                letter=matched.group(3),
                password=matched.group(4)
            ))

    def part1(self):
        result = 0

        for password in self.passwords:
            count = len(list(filter(lambda x: x == password.letter, password.password)))
            if password.min <= count <= password.max:
                result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        for password in self.passwords:
            first_equals = password.password[password.min-1] == password.letter
            second_equals = password.password[password.max-1] == password.letter

            if (first_equals and not second_equals) or (second_equals and not first_equals):
                result += 1

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D2("2020/2.txt")
    code.part1()
    code.part2()
