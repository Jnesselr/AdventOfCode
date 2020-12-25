from typing import List


class KnotHash(object):
    def __init__(self, data):
        self._circle: List[int] = list(range(256))
        self._circle_size = len(self._circle)
        self._data = [ord(x) for x in data] + [17, 31, 73, 47, 23]

        self._current_position = 0
        self._skip_size = 0

        for _ in range(64):
            self._one_round()

        self._dense_hash = [0] * 16
        for block in range(16):
            for index in range(16):
                self._dense_hash[block] ^= self._circle[16 * block + index]

        self._hex_string = ""

        for h in self._dense_hash:
            self._hex_string += "{:02x}".format(h)

    def _one_round(self):
        for length in self._data:
            for i in range(length // 2):
                from_index: int = (self._current_position + i) % self._circle_size
                to_index: int = (self._current_position + length - i - 1) % self._circle_size
                temp: int = self._circle[from_index]
                self._circle[from_index] = self._circle[to_index]
                self._circle[to_index] = temp

            self._current_position = (self._current_position + length + self._skip_size) % self._circle_size
            self._skip_size += 1

    @property
    def hex(self):
        return self._hex_string
