from aoc.util.inputs import Input


class Y2015D11(object):
    def __init__(self, file_name):
        self.current_password = Input(file_name).line()

        good_password_generator = self._generator()
        self.next_good_password = next(good_password_generator)
        self.next_next_good_password = next(good_password_generator)

    def part1(self):
        result = self.next_good_password

        print("Part 1:", result)

    def part2(self):
        result = self.next_next_good_password

        print("Part 2:", result)

    def _generator(self):
        password = self.current_password
        while True:
            plist = list(password)
            index = len(password) - 1
            rollover = True
            while rollover:
                if plist[index] == 'z':
                    plist[index] = 'a'
                    index -= 1
                else:
                    rollover = False
                    plist[index] = chr(ord(plist[index])+1)
            password = "".join(plist)

            if 'i' in password or 'o' in password or 'l' in password:
                continue

            straight_run = False
            for index in range(len(password)-2):
                if ord(password[index]) + 2 == ord(password[index+1]) + 1 == ord(password[index+2]):
                    straight_run = True

            if not straight_run:
                continue

            double_pair = False
            for x in range(len(password)-4):
                for y in range(x+2, len(password)-1):
                    if password[x] == password[x+1] and password[y] == password[y+1]:
                        double_pair = True

            if not double_pair:
                continue

            yield password


if __name__ == '__main__':
    code = Y2015D11("2015/11.txt")
    code.part1()
    code.part2()
