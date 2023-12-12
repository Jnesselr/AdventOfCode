from dataclasses import dataclass

from aoc.util.inputs import Input


@dataclass(frozen=True)
class SpringRow:
    record: str
    check: tuple[int, ...]

    @property
    def complete(self) -> bool:
        return len(self.record) == 0 and len(self.check) == 0

    def normalized(self) -> 'SpringRow':
        """

        :return: a SpringRow with all prefixed '.' removed
        """
        if len(self.record) == 0 or self.record[0] != '.':
            return self

        index = 0
        while index < len(self.record) and self.record[index] == '.':
            index += 1

        return SpringRow(
            record=self.record[index:],
            check=self.check
        )

    def options(self) -> list['SpringRow']:
        """

        :return: The options that are at least valid with what we know. If a SpringRow is not complete and no options
        are returned, then that SpringRow is invalid.
        """
        if self.complete:
            return []

        first_mystery = self.record.find('?')
        first_damaged = self.record.find('#')

        if first_mystery == -1 and first_damaged == -1 and len(self.check) > 0:
            return []  # No mystery or damaged but still some to check, this can't be valid

        first_index = len(self.record)
        if first_mystery != -1:
            first_index = first_mystery
        if first_damaged != -1 and first_damaged < first_index:
            first_index = first_damaged

        result = []
        if first_index == first_mystery:
            # Replace all ? with . if we start with a mystery and never run into a damaged section. Special case.
            list_record = list(self.record)
            mystery_index = first_mystery
            while True:
                list_record[mystery_index] = '.'
                mystery_index += 1

                if mystery_index == len(self.record) or self.record[mystery_index] != '?':
                    break

            if mystery_index < first_damaged or first_damaged == -1:
                # It MIGHT be valid to replace current section of ? with .
                result.append(SpringRow(
                    record=''.join(list_record[mystery_index:]),
                    check=self.check
                ).normalized())

        # If we have nothing to check for, we'll only return what we've collected so far or nothing at all if there are
        # further damages
        if len(self.check) == 0:
            if any(ch == '#' for ch in self.record):
                return []  # Nothing to check for but we still have damages

            return result

        # Find the first index with '.' past our first mystery or damage
        last_index = first_index
        while (last_index + 1) < len(self.record) and self.record[last_index + 1] != '.':
            last_index += 1

        # How much damage are we expecting?
        expected_group_length = self.check[0]

        # For our sliding window, fill it in and add it to the results if it would be valid
        for index in range(first_index, last_index - expected_group_length + 2):
            list_record = list(self.record)
            if any(self.record[i] == '#' for i in range(first_index, index)):
                continue  # Can't put an operational one over a damaged one before our range

            after_range_index = index + expected_group_length
            if after_range_index < len(self.record):
                if self.record[after_range_index] == '#':
                    continue  # Can't put an operational one over a damaged one after our range
                list_record[after_range_index] = '.'

            for i in range(first_index, index):
                list_record[i] = '.'  # ? or . -> .

            for i in range(expected_group_length):
                list_record[index + i] = '#'  # ? or # -> #

            new_record = ''.join(list_record[after_range_index + 1:])
            if '#' in new_record and len(self.check) == 1:
                # Don't add that Spring Row, it will definitely be invalid. There will be nothing to check next round
                # and we'll still have a damaged section.
                continue

            result.append(SpringRow(
                record=new_record,
                check=self.check[1:],
            ).normalized())

        return result

    def unfolded(self):
        return SpringRow(
            record='?'.join(self.record for _ in range(5)),
            check=self.check * 5
        )


class Y2023D12(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.rows: list[SpringRow] = []

        for line in lines:
            record, check = line.split(' ')
            check = [int(x) for x in check.split(',')]

            self.rows.append(SpringRow(record, tuple(check)))

        # Cache key is record and remaining records
        self._cache: dict[SpringRow, int] = {}

    def part1(self):
        result = 0

        for row in self.rows:
            result += self._find_valid_combos(row)

        print("Part 1:", result)

    def part2(self):
        result = 0

        for row in self.rows:
            result += self._find_valid_combos(row.unfolded())

        print("Part 2:", result)

    def _find_valid_combos(self, row: SpringRow) -> int:
        if row in self._cache:
            return self._cache[row]

        if row.complete:
            self._cache[row] = 1
            return self._cache[row]

        result = 0
        options = row.options()
        results = []
        for option in options:
            combos = self._find_valid_combos(option)
            result += combos
            results.append(combos)
        self._cache[row] = result

        return result


if __name__ == '__main__':
    code = Y2023D12("2023/12.txt")
    code.part1()
    code.part2()
