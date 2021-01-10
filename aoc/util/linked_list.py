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
