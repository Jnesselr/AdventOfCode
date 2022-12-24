from aoc.util.coordinate import Turtle, TurtleDirection, Coordinate
from aoc.util.inputs import Input


class Y2020D12(object):
    def __init__(self, file_name):
        self.lines = Input(file_name).lines()

    def part1(self):
        ship = Turtle(direction=TurtleDirection.EAST)

        for line in self.lines:
            value = int(line[1:])
            command = line[0]
            if command == "N":
                ship = ship.world_up(value)
            elif command == "S":
                ship = ship.world_down(value)
            elif command == "E":
                ship = ship.world_right(value)
            elif command == "W":
                ship = ship.world_left(value)
            elif command == "L":
                ship = ship.turn_left(value // 90)
            elif command == "R":
                ship = ship.turn_right(value // 90)
            elif command == "F":
                ship = ship.forward(value)

        result = ship.coordinate.manhattan(Coordinate(0, 0))

        print("Part 1:", result)

    def part2(self):
        waypoint = Coordinate(10, 1)
        ship = Coordinate(0, 0)

        for line in self.lines:
            value = int(line[1:])
            command = line[0]
            if command == "N":
                waypoint = waypoint.up(value)
            elif command == "S":
                waypoint = waypoint.down(value)
            elif command == "E":
                waypoint = waypoint.right(value)
            elif command == "W":
                waypoint = waypoint.left(value)
            elif command == "L":
                waypoint = waypoint.ccw_around(ship, value // 90)
            elif command == "R":
                waypoint = waypoint.cw_around(ship, value // 90)
            elif command == "F":
                diff_coordinate = waypoint - ship
                ship = ship + (diff_coordinate * value)
                waypoint = ship + diff_coordinate

        result = ship.manhattan(Coordinate(0, 0))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D12("2020/12.txt")
    code.part1()
    code.part2()
