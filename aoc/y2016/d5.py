import hashlib
import itertools

from aoc.util.inputs import Input


class Y2016D5(object):
    def __init__(self, file_name):
        self.door_id = Input(file_name).line()

        self.password_ordered = ""
        self.password_by_position = [" "] * 8

        for i in itertools.count():
            md5_hex = hashlib.md5(f'{self.door_id}{i}'.encode()).hexdigest()

            if md5_hex[:5] == '00000':
                if len(self.password_ordered) < 8:
                    self.password_ordered += md5_hex[5]

                position = int(md5_hex[5], 16)
                if position >= 8:
                    continue
                if self.password_by_position[position] == " ":
                    self.password_by_position[position] = md5_hex[6]

            if len(self.password_ordered) == 8 and not " " in self.password_by_position:
                break

        self.password_by_position = "".join(self.password_by_position)

    def part1(self):
        result = self.password_ordered

        print("Part 1:", result)

    def part2(self):
        result = self.password_by_position

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D5("2016/5.txt")
    code.part1()
    code.part2()
