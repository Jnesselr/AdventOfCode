from typing import Callable, Optional, Dict


class BinarySearch(object):
    def __init__(self, function: Callable[[int], bool]):
        self._function = function
        self._cache: Dict[int, bool] = {}

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

        if self.test(start):
            return start
        elif self.test(end):
            return end
        return None

    def test(self, value) -> bool:
        if value not in self._cache:
            self._cache[value] = self._function(value)

        return self._cache[value]

    def earliest(self, start: int, change: Callable[[int], int]):
        previous = start
        current = start

        while not self.test(current):
            previous = current
            current = change(current)

        new_search = BinarySearch(lambda x: not self.test(x))
        result = new_search.find(previous, current)
        # If we can't find a value that's not true in new_search, previous is our oldest
        if result is None:
            return previous
        return result + 1

    def latest(self, start: int, change: Callable[[int], int]):
        previous = start
        current = start

        while self._function(current):
            previous = current
            current = change(current)

        return self.find(previous, current)
