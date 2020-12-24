from aoc.util.inputs import Input


class GarbageCollector(object):
    def __init__(self, line):
        self.ignored_count = 0
        self.score = 0

        index = 0
        within_garbage = False
        group_depth = 0
        while index < len(line):
            character = line[index]

            if within_garbage:
                if character == '!':
                    index += 1
                elif character == '>':
                    within_garbage = False
                else:
                    self.ignored_count += 1
            elif character == '{':
                group_depth += 1
            elif character == '}':
                self.score += group_depth
                group_depth -= 1
            elif character == '<':
                within_garbage = True
            elif character == '!':
                index += 1

            index += 1


class Y2017D9(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        self.garbage_collector = GarbageCollector(line)

    def part1(self):
        result = self.garbage_collector.score

        print("Part 1:", result)

    def part2(self):
        result = self.garbage_collector.ignored_count

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D9("2017/9.txt")
    code.part1()
    code.part2()
