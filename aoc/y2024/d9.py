import heapq
from typing import Tuple

from aoc.util.inputs import Input


class Y2024D9(object):
    def __init__(self, file_name):
        self._initial_disk_state = Input(file_name).line()
        self._disk_map: dict[int, int] = {}  # block index -> id

        # Used in part 1
        self._files: list[Tuple[int, int]] = []  # (-block id, fild id)
        self._blanks: list[int] = []  # block id

        # Used in part 2
        self._blank_lengths: dict[int, list[Tuple[int, int]]] = {x: [] for x in range(1, 10)}
        self._file_lengths: list[Tuple[int, int, int]] = []  # (- file id, block start, length)

        id_number = 0
        block_id = 0
        is_file = True
        for character in self._initial_disk_state:
            length = int(character)

            if is_file:
                heapq.heappush(self._file_lengths, (-id_number, block_id, length))
                for _ in range(length):
                    heapq.heappush(self._files, (-block_id, id_number))
                    self._disk_map[block_id] = id_number
                    block_id += 1
                id_number += 1
            elif length > 0:
                for i in range(1, length + 1):
                    heapq.heappush(self._blank_lengths[i], (block_id, length))

                for _ in range(length):
                    heapq.heappush(self._blanks, block_id)
                    block_id += 1

            is_file = not is_file

    def part1(self):
        disk_map = self._disk_map.copy()

        while len(self._blanks) > 0:
            next_blank = heapq.heappop(self._blanks)
            next_file = heapq.heappop(self._files)
            file_block_id = -next_file[0]

            if next_blank > file_block_id:
                break

            file_id = next_file[1]
            del disk_map[file_block_id]
            disk_map[next_blank] = file_id

        result = sum([block_id * file_number for (block_id, file_number) in disk_map.items()])

        print("Part 1:", result)

    def part2(self):
        disk_map = self._disk_map.copy()

        while len(self._file_lengths) > 0:
            _, file_start, length = heapq.heappop(self._file_lengths)
            heapq.heapify(self._blank_lengths[length])  # This is probably so inefficient
            best_fit_list = self._blank_lengths[length]
            if len(best_fit_list) == 0:
                continue  # Nothing to do, we can't move a file of this length

            best_fit = best_fit_list[0]
            blank_start, blank_length = best_fit

            if blank_start > file_start:
                # Can't move it to the right, so we ignore this file
                # Save time because we will NEVER be able to move a file of this size to the left again
                self._blank_lengths[length] = []
                continue

            # To move the file, let's first remove this blank from all the places where it might exist
            for i in range(1, blank_length + 1):
                self._blank_lengths[i].remove(best_fit)

            # Then we can put the new blank in all the places it needs to be
            new_blank_length = blank_length - length
            new_blank_start = blank_start + length
            for i in range(1, new_blank_length + 1):
                self._blank_lengths[i].append((new_blank_start, new_blank_length))

            # Now that our blanks are fixed, we will fix the disk map to move the file
            for i in range(length):
                disk_map[blank_start + i] = disk_map[file_start + i]
                del disk_map[file_start + i]

            # self.disk_print(disk_map)

        result = sum([block_id * file_number for (block_id, file_number) in disk_map.items()])

        print("Part 2:", result)

    @staticmethod
    def disk_print(disk_map: dict[int, int]):
        for i in range(max(disk_map.keys()) + 1):
            if i in disk_map:
                print(disk_map[i], end='')
            else:
                print('.', end='')
        print()


if __name__ == '__main__':
    code = Y2024D9("2024/9.txt")
    code.part1()
    code.part2()
