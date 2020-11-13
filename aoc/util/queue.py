import heapq
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List

T = TypeVar('T')


@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    priority: int
    item: T = field(compare=False)


class PriorityQueue(Generic[T]):
    def __init__(self):
        self._elements: List[PrioritizedItem[T]] = []

    def empty(self) -> bool:
        return len(self._elements) == 0

    def push(self, item: T, priority: int):
        heapq.heappush(self._elements, PrioritizedItem[T](priority, item))

    def pop(self):
        return heapq.heappop(self._elements).item

    def __bool__(self):
        return not self.empty()
