import re
from dataclasses import dataclass

from aoc.util.chinese_remainder import ChineseRemainderTheorem
from aoc.util.inputs import Input


@dataclass
class Disk(object):
    number: int
    positions: int
    time_0_position: int


class Y2016D15(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.disks = []
        for line in lines:
            matched = re.match(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', line)
            self.disks.append(Disk(
                number=int(matched.group(1)),
                positions=int(matched.group(2)),
                time_0_position=int(matched.group(3))
            ))

    def part1(self):
        crt = ChineseRemainderTheorem()

        for disk in self.disks:
            crt.a_mod_n(-disk.number - disk.time_0_position, disk.positions)

        result = crt.result

        print("Part 1:", result)

    def part2(self):
        crt = ChineseRemainderTheorem()

        disks_copy = self.disks.copy()
        disks_copy.append(Disk(
            number=max(self.disks, key=lambda x: x.number).number + 1,
            positions=11,
            time_0_position=0
        ))

        for disk in disks_copy:
            crt.a_mod_n(-disk.number - disk.time_0_position, disk.positions)

        result = crt.result

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D15("2016/15.txt")
    code.part1()
    code.part2()
