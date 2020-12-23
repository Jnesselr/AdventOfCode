from __future__ import annotations

from typing import Optional

from aoc.util.inputs import Input


class LinkedListNode(object):
    def __init__(self, value: int):
        self.value = value
        self.prev: LinkedListNode = self
        self.next: LinkedListNode = self

    def append(self, value: int) -> LinkedListNode:
        next_node = self.next
        new_node = LinkedListNode(value)

        new_node.next = next_node
        next_node.prev = new_node

        new_node.prev = self
        self.next = new_node

        return new_node

    def remove(self) -> None:
        prev_node = self.prev
        next_node = self.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def find(self, value) -> Optional[LinkedListNode]:
        if self.value == value:
            return value

        node = self.next
        while node != self:
            if node.value == value:
                return node
            node = node.next

        return None


class CrabGame(object):
    def __init__(self, line, crab_is_an_asshole=False):
        self._line = line
        self._lookup = {}

        self.highest_value = 0
        value = int(line[0])
        self.highest_value = max(value, self.highest_value)
        self.current_node = LinkedListNode(value)
        self._lookup[value] = self.current_node

        node = self.current_node
        for value in line[1:]:
            value = int(value)
            node = node.append(value)
            self._lookup[value] = node
            self.highest_value = max(value, self.highest_value)

        if crab_is_an_asshole:
            for i in range(1000000 - len(line)):
                value = self.highest_value + 1
                self.highest_value = max(value, self.highest_value)
                node = node.append(value)
                self._lookup[value] = node

    @property
    def node_str(self):
        result = ""

        result += str(self.current_node.value)
        node = self.current_node.next
        while node != self.current_node:
            result += str(node.value)
            node = node.next

        return result

    @property
    def next_two_cups_product(self):
        one_cup = self._lookup[1]
        return one_cup.next.value * one_cup.next.next.value

    def play(self, rounds):
        for i in range(rounds):
            current_value = self.current_node.value
            a_node = self.current_node.next
            a_node.remove()
            a_value = a_node.value
            b_node = self.current_node.next
            b_node.remove()
            b_value = b_node.value
            c_node = self.current_node.next
            c_node.remove()
            c_value = c_node.value

            next_value = current_value - 1
            while next_value in [0, a_value, b_value, c_value]:
                next_value = next_value-1
                if next_value <= 0:
                    next_value = self.highest_value

            inserting_node = self._lookup[next_value]
            a_node = inserting_node.append(a_value)
            self._lookup[a_value] = a_node
            b_node = a_node.append(b_value)
            self._lookup[b_value] = b_node
            c_node = b_node.append(c_value)
            self._lookup[c_value] = c_node

            self.current_node = self.current_node.next


class Y2020D23(object):
    def __init__(self, file_name):
        self.input = Input(file_name).line()

    def part1(self):
        game = CrabGame(self.input)
        game.play(100)
        node_str = game.node_str
        one_location = node_str.find('1')
        result = node_str[one_location+1:] + node_str[:one_location]

        print("Part 1:", result)

    def part2(self):
        game = CrabGame(self.input, crab_is_an_asshole=True)
        game.play(10000000)
        result = game.next_two_cups_product

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D23("2020/23.txt")
    code.part1()
    code.part2()
