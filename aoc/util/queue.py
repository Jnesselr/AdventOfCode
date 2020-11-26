import heapq
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List, Iterator

T = TypeVar('T')


@dataclass(order=True)
class PrioritizedItem(Generic[T]):
    priority: int
    counter: int
    item: T = field(compare=False)


class PriorityQueue(Generic[T]):
    def __init__(self):
        self._elements: List[PrioritizedItem[T]] = []
        self._counter = 0
        self._element_count = 0

    @property
    def empty(self) -> bool:
        return self._element_count == 0

    def push(self, item: T, priority: int):
        heapq.heappush(self._elements, PrioritizedItem[T](priority, self._counter, item))
        self._counter += 1
        self._element_count += 1

    def pop(self) -> T:
        self._element_count -= 1
        return heapq.heappop(self._elements).item

    def __bool__(self) -> bool:
        return not self.empty

    def __len__(self):
        return self._elements.__len__()
