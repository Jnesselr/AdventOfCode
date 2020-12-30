from aoc.util.inputs import Input


class Y2016Y9(object):
    def __init__(self, file_name):
        self.input = Input(file_name).line()

    def part1(self):
        result = self._decode_count(self.input, False)

        print("Part 1:", result)

    def part2(self):
        result = self._decode_count(self.input, True)

        print("Part 2:", result)

    @classmethod
    def _decode_count(cls, line, recursive) -> int:
        index = 0
        result = 0

        while index < len(line):
            character = line[index]
            if character == '(':
                end_index = index
                while line[end_index] != ')':
                    end_index += 1

                length, times = line[index + 1:end_index].split('x')
                length = int(length)
                repeat_sequence = line[end_index + 1:end_index + length + 1]
                if recursive:
                    sequence_length = cls._decode_count(repeat_sequence, recursive)
                else:
                    sequence_length = len(repeat_sequence)
                result += int(times) * sequence_length

                index = end_index + length + 1
            else:
                result += 1
                index += 1

        return result


if __name__ == '__main__':
    code = Y2016Y9("2016/9.txt")
    code.part1()
    code.part2()
