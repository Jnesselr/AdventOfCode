from dataclasses import dataclass, field
from math import prod
from typing import Optional, List

from aoc.util.inputs import Input


@dataclass
class Packet(object):
    version: int
    type_id: int
    literal: Optional[int] = field(default=None)
    sub_packets: List['Packet'] = field(default_factory=lambda: [])

    @property
    def sum_version(self) -> int:
        return self.version + sum(x.sum_version for x in self.sub_packets)

    @property
    def value(self) -> int:
        sub_values = [x.value for x in self.sub_packets]
        if self.type_id == 0:
            return sum(sub_values)
        elif self.type_id == 1:
            return prod(sub_values)
        elif self.type_id == 2:
            return min(sub_values)
        elif self.type_id == 3:
            return max(sub_values)
        elif self.type_id == 4:
            return self.literal
        elif self.type_id == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.type_id == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.type_id == 7:
            return 1 if sub_values[0] == sub_values[1] else 0


class BitStream(object):
    def __init__(self, data: str):
        self._data = data
        self._data_index = 0
        self._bit_index = 0
        self._current_bits: Optional[str] = None
        self._total_bit_index = 0

    def __iter__(self):
        return self

    def packet(self) -> Packet:
        version = self.read(3)
        type_id = self.read(3)

        if type_id == 4:
            value = 0
            segment = self.read(5)
            while True:
                value <<= 4
                value += (segment & 0xF)

                if segment & 16 == 0:
                    break

                segment = self.read(5)

            return Packet(
                version=version,
                type_id=type_id,
                literal=value
            )

        length_type_id = self.read(1)
        sub_packets = []
        if length_type_id == 0:
            length_of_sub_packets = self.read(15)
            current_index = self._total_bit_index
            while (self._total_bit_index - current_index) < length_of_sub_packets:
                sub_packets.append(self.packet())
        else:
            num_sub_packets = self.read(11)
            for _ in range(num_sub_packets):
                sub_packets.append(self.packet())

        return Packet(
            version=version,
            type_id=type_id,
            sub_packets=sub_packets
        )

    def read(self, bit_count: int) -> int:
        result = 0

        for _ in range(bit_count):
            result <<= 1
            result += next(self)

        return result

    @staticmethod
    def _to_bits(value: str) -> str:
        if value >= 'A':
            result = bin(ord(value) - ord('A') + 10)[2:]
        else:
            result = bin(ord(value) - ord('0'))[2:]

        result = ("0" * (4 - len(result))) + result

        return result

    def __next__(self) -> int:
        if self._data_index >= len(self._data):
            raise StopIteration

        if self._current_bits is None:
            self._current_bits = self._to_bits(self._data[self._data_index])

        value = int(self._current_bits[self._bit_index])

        self._bit_index += 1
        self._total_bit_index += 1

        if self._bit_index == 4:
            self._bit_index = 0
            self._data_index += 1
            self._current_bits = None

        return value


class Y2021D16(object):
    def __init__(self, file_name):
        _input = Input(file_name).line()
        stream = BitStream(_input)

        self._packet = stream.packet()

    def part1(self):
        result = self._packet.sum_version

        print("Part 1:", result)

    def part2(self):
        result = self._packet.value

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2021D16("2021/16.txt")
    code.part1()
    code.part2()
