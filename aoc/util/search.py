from typing import Callable, Optional, Dict, Generic, Type, TypeVar


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


class MinSearch(object):
    def __init__(self, function: Callable[[int], int]):
        self._function = function
        self._cache: Dict[int, int] = {}

    def test(self, value: int) -> int:
        if value not in self._cache:
            self._cache[value] = self._function(value)

        return self._cache[value]

    def min(self, start: int) -> int:
        start_y = self.test(start)
        plus_y = self.test(start + 1)
        minus_y = self.test(start - 1)

        if start_y < plus_y and start_y < minus_y:
            return start
        elif minus_y > start_y > plus_y:
            # Moving towards positive
            diff = 1
            test_x = start + diff
            while self.test(test_x) > self.test(test_x + 1):
                diff *= 2
                test_x += diff
            left = start
            right = test_x
        else:
            # Moving towards negative
            diff = 1
            test_x = start - diff
            while self.test(test_x) > self.test(test_x + 1):
                diff *= 2
                test_x -= diff
            left = test_x
            right = start

        while left + 1 < right:
            current = (left + right) // 2
            value = self.test(current)
            value_minus = self.test(current-1)
            value_plus = self.test(current+1)
            if value < value_minus and value < value_plus:
                return current
            elif value_minus < value < value_plus:
                right = current
            else:
                left = current
