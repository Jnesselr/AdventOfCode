from typing import Callable, Optional


class BinarySearch(object):
    def __init__(self, function: Callable[[int], bool]):
        self._function = function

    def find(self, start: int, end: int) -> Optional[int]:
        """
        Use a binary search to find the latest value that our function returns True
        """
        while start + 1 < end:
            current = (start + end) // 2
            valid = self._function(current)

            if valid:
                start = current
            else:
                end = current

        if self._function(start):
            return start
        elif self._function(end):
            return end
        return None

    def earliest(self, start: int, change: Callable[[int], int]):
        previous = start
        current = start

        while not self._function(current):
            previous = current
            current = change(current)

        new_search = BinarySearch(lambda x: not self._function(x))
        return new_search.find(previous, current) + 1

    def latest(self, start: int, change: Callable[[int], int]):
        previous = start
        current = start

        while self._function(current):
            previous = current
            current = change(current)

        return self.find(previous, current)
