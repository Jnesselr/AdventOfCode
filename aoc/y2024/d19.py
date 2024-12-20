import functools

from aoc.util.inputs import Input


class Y2024D19(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()
        available_towels: set[str] = set(groups[0][0].split(', '))
        self._wanted_towels: list[str] = groups[1]

        self._terminal_node = "<terminal>"
        self._towel_trie = {}  # Recursive dictionary

        def _fill_trie(trie, _sub_towel):
            if len(_sub_towel) == 0:
                trie[self._terminal_node] = None
            else:
                color = _sub_towel[0]
                if color not in trie:
                    trie[color] = {}
                _fill_trie(trie[color], _sub_towel[1:])

        for towel in available_towels:
            _fill_trie(self._towel_trie, towel)

    def part1(self):
        result = sum(1 for t in self._wanted_towels if self._arrangement_count(t) > 0)

        print("Part 1:", result)

    def part2(self):
        result = sum(self._arrangement_count(t) for t in self._wanted_towels)

        print("Part 2:", result)

    @functools.cache
    def _arrangement_count(self, towel: str) -> int:
        # We only want to cache based on the towel. I think it will work either way, but this feels simpler for the
        # recursive calls.
        return self.__arrangement_count(towel, self._towel_trie)

    def __arrangement_count(self, towel: str, trie: dict) -> int:
        if len(towel) == 0:
            return 1 if self._terminal_node in trie else 0

        result = 0
        if self._terminal_node in trie:
            # The towel parts we chopped off would make a valid towel. Now we ask the number of arrangements for the
            # remaining potential towel as if it was just called on its own
            result += self._arrangement_count(towel)

        color = towel[0]
        if color in trie:
            result += self.__arrangement_count(towel[1:], trie[color])

        return result


if __name__ == '__main__':
    code = Y2024D19("2024/19.txt")
    code.part1()
    code.part2()
