from typing import Optional

from aoc.util.inputs import Input
from aoc.util.linked_list import LinkedListNode

IndexedValue = tuple[int, int]  # Index, Value


class Y2022D20(object):
    def __init__(self, file_name):
        self.input_list = Input(file_name).ints()

    def _get_zero(self) -> LinkedListNode[IndexedValue]:
        circular_buffer_zero: Optional[LinkedListNode[IndexedValue]] = None
        head = None
        for index, value in enumerate(self.input_list):
            node_value = (index, value)
            if head is None:
                head = LinkedListNode[IndexedValue](node_value)
            else:
                head = head.append(node_value)

            if value == 0:
                circular_buffer_zero = head

        return circular_buffer_zero

    def _mix(self, circular_buffer_zero: LinkedListNode[IndexedValue], decryption_key=1):
        for index, value in enumerate(self.input_list):
            node_value = (index, value)
            item_node = circular_buffer_zero.find(node_value)
            value = (value * decryption_key) % (len(self.input_list) - 1)
            if value > 0:
                for _ in range(value):
                    item_node.swap_with_right()
            else:
                for _ in range(-value):
                    item_node.swap_with_left()

    def part1(self):
        circular_buffer_zero = self._get_zero()
        self._mix(circular_buffer_zero)

        a = circular_buffer_zero.skip(1_000).value[1]
        b = circular_buffer_zero.skip(2_000).value[1]
        c = circular_buffer_zero.skip(3_000).value[1]

        result = a + b + c

        print("Part 1:", result)

    def part2(self):
        circular_buffer_zero = self._get_zero()

        key = 811589153
        for i in range(10):
            self._mix(circular_buffer_zero, decryption_key=key)
            print(i)

        a = circular_buffer_zero.skip(1_000).value[1] * key
        b = circular_buffer_zero.skip(2_000).value[1] * key
        c = circular_buffer_zero.skip(3_000).value[1] * key

        result = a + b + c

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2022D20("2022/20.txt")
    code.part1()
    code.part2()
