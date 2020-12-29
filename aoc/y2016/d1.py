from aoc.util.coordinate import Turtle, TurtleDirection
from aoc.util.inputs import Input


class Y2016D1(object):
    def __init__(self, file_name):
        line = Input(file_name).line()

        self.moves = line.split(', ')

    def part1(self):
        turtle = Turtle(direction=TurtleDirection.NORTH)

        for move in self.moves:
            if move[0] == 'R':
                turtle = turtle.turn_right()
            else:
                turtle = turtle.turn_left()

            turtle = turtle.forward(int(move[1:]))

        result = abs(turtle.coordinate.x) + abs(turtle.coordinate.y)

        print("Part 1:", result)

    def part2(self):
        seen = set()
        turtle = Turtle(direction=TurtleDirection.NORTH)
        seen.add(turtle.coordinate)

        result = 0
        for move in self.moves:
            if result != 0:
                break
            if move[0] == 'R':
                turtle = turtle.turn_right()
            else:
                turtle = turtle.turn_left()

            for _ in range(int(move[1:])):
                turtle = turtle.forward()
                if turtle.coordinate in seen:
                    result = abs(turtle.coordinate.x) + abs(turtle.coordinate.y)
                    break
                seen.add(turtle.coordinate)

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2016D1("2016/1.txt")
    code.part1()
    code.part2()
