import re
from collections import Counter
from dataclasses import dataclass
from typing import List

from aoc.util.inputs import Input


@dataclass(frozen=True)
class Room(object):
    name: str
    sector_id: int
    checksum: str

    @property
    def is_real(self) -> bool:
        most_common = Counter(self.name.replace('-', '')).most_common()
        most_common = sorted(most_common, key=lambda x: (-x[1], x[0]))
        checksum = "".join(x[0] for x in most_common[:5])
        return self.checksum == checksum

    @property
    def decoded(self) -> str:
        return "".join(
            chr((((ord(x) - 97) + self.sector_id) % 26) + 97)
            if x != '-' else ' '
            for x in self.name
        )


class Y2016D4(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        rooms: List[Room] = []

        for line in lines:
            matched = re.match(r'([\w-]+)-(\d+)\[(\w+)]', line)
            name = matched.group(1)
            sector_id = int(matched.group(2))
            checksum = matched.group(3)
            rooms.append(Room(name, sector_id, checksum))

        self.valid_rooms = [room for room in rooms if room.is_real]

    def part1(self):
        result = sum(room.sector_id for room in self.valid_rooms)

        print("Part 1:", result)

    def part2(self):
        result = [room.sector_id for room in self.valid_rooms if room.decoded == "northpole object storage"].pop()

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D4("2016/4.txt")
    code.part1()
    code.part2()
