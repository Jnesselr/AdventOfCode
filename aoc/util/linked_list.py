from __future__ import annotations

from typing import Optional, TypeVar, Generic

T = TypeVar('T')


class LinkedListNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.prev: LinkedListNode[T] = self
        self.next: LinkedListNode[T] = self

    def append(self, value: T) -> LinkedListNode[T]:
        next_node = self.next
        new_node = LinkedListNode[T](value)

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

    def find(self, value) -> Optional[LinkedListNode[T]]:
        if self.value == value:
            return value

        node = self.next
        while node != self:
            if node.value == value:
                return node
            node = node.next

        return None

    def swap_with_right(self):
        right_node = self.next
        left_node = self.prev

        self.next = right_node.next
        self.next.prev = self

        self.prev = right_node
        self.prev.next = self

        right_node.prev = left_node
        left_node.next = right_node

    def swap_with_left(self):
        right_node = self.next
        left_node = self.prev

        self.prev = left_node.prev
        self.prev.next = self

        self.next = left_node
        self.next.prev = self

        right_node.prev = left_node
        left_node.next = right_node

    def skip(self, amount: int) -> LinkedListNode[T]:
        result = self

        for _ in range(abs(amount)):
            if amount > 0:
                result = result.next
            else:
                result = result.prev

        return result
