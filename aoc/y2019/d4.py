from aoc.util.inputs import Input


class Y2019D4(object):
    def __init__(self, file_name):
        line = Input(file_name).line()
        array = line.split('-')
        self.start = int(array[0])
        self.end = int(array[1])

    def part1(self):
        result = 0

        for password in range(self.start, self.end + 1):
            valid = self._two_adjacent_digits(password)
            valid &= self._increasing_digits(password)

            if valid:
                result += 1

        print("Part 1:", result)

    def part2(self):
        result = 0

        for password in range(self.start, self.end + 1):
            valid = self._no_triple_digits(password)
            valid &= self._increasing_digits(password)

            if valid:
                result += 1

        print("Part 2:", result)

    @staticmethod
    def _two_adjacent_digits(password):
        password = str(password)

        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                return True
        return False

    @staticmethod
    def _increasing_digits(password):
        password = str(password)

        for i in range(len(password) - 1):
            if int(password[i]) > int(password[i + 1]):
                return False
        return True

    @staticmethod
    def _no_triple_digits(password):
        password = str(password)

        current_run = 1
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                current_run += 1
            elif current_run == 2:
                return True
            else:
                current_run = 1

        if current_run == 2:
            return True
        return False



if __name__ == '__main__':
    code = Y2019D4("2019/4.txt")
    code.part1()
    code.part2()
