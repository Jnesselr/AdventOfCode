import enum
import functools
import json
from itertools import zip_longest
from typing import List, Tuple, Any

from aoc.util.inputs import Input


class OrderResult(enum.Enum):
    SAME = enum.auto()
    ORDERED = enum.auto()
    UNORDERED = enum.auto()


class Y2022D14(object):
    def __init__(self, file_name):
        packet_strings = Input(file_name).grouped()

        self._packets: List[Tuple[Any, Any]] = []
        for group in packet_strings:
            self._packets.append((
                json.loads(group[0]),
                json.loads(group[1])
            ))

    def _get_order(self, left, right) -> OrderResult:
        for left_value, right_value in zip_longest(left, right):
            if left_value is None:  # If the left list runs out of items first, the inputs are in the right order.
                return OrderResult.ORDERED
            if right_value is None:  # If the right list runs out of items first, the inputs are not in the right order.
                return OrderResult.UNORDERED

            if isinstance(left_value, int) and isinstance(right_value, int):
                if left_value < right_value:
                    return OrderResult.ORDERED
                elif left_value > right_value:
                    return OrderResult.UNORDERED
                else:
                    # Same, continue
                    continue

            if isinstance(left_value, int):
                left_value = [left_value]

            if isinstance(right_value, int):
                right_value = [right_value]

            sub_result = self._get_order(left_value, right_value)
            if sub_result != OrderResult.SAME:
                return sub_result

        return OrderResult.SAME

    def part1(self):
        result = 0
        for index, packets in enumerate(self._packets):
            o_result = self._get_order(packets[0], packets[1])
            if o_result == OrderResult.ORDERED:
                result += index + 1

        print("Part 1:", result)

    def part2(self):
        divider_2 = [[2]]
        divider_6 = [[6]]
        all_packets = [divider_2, divider_6]
        for left, right in self._packets:
            all_packets.append(left)
            all_packets.append(right)

        def _cmp(x, y):
            o_result = self._get_order(x, y)
            if o_result == OrderResult.SAME:
                return 0
            elif o_result == OrderResult.UNORDERED:
                return 1
            elif o_result == OrderResult.ORDERED:
                return -1

        all_packets = sorted(all_packets, key=functools.cmp_to_key(_cmp))

        index_2 = all_packets.index(divider_2) + 1
        index_6 = all_packets.index(divider_6) + 1
        result = index_2 * index_6

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D14("2022/13.txt")
    code.part1()
    code.part2()
