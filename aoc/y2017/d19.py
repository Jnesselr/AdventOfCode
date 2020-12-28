from aoc.util.coordinate import Turtle, TurtleDirection
from aoc.util.inputs import Input


class Y2017D19(object):
    def __init__(self, file_name):
        self.grid = Input(file_name).grid()

        self.starting_coordinate = min(self.grid.find('|'))

        turtle = Turtle(direction=TurtleDirection.DOWN, coordinate=self.starting_coordinate)

        self.secret_message = ""
        self.step_count = 0

        while True:
            next_turtle = turtle.forward()
            self.step_count += 1  # We probably moved forward, but we might have to turn instead

            current_character = self.grid[next_turtle.coordinate]
            if current_character in [None, ' ']:
                found_next_path = False

                for direction_turtle in [turtle.turn_left(), turtle.turn_right()]:
                    neighbor_turtle = direction_turtle.forward()
                    if neighbor_turtle.coordinate == turtle.coordinate:
                        continue  # Don't go backwards

                    if self.grid[neighbor_turtle.coordinate] not in [None, ' ']:
                        found_next_path = True
                        next_turtle = direction_turtle
                        self.step_count -= 1  # Turns out, we didn't move forward, we turned
                        break

                if not found_next_path:
                    break
            elif current_character.isalpha():
                self.secret_message += current_character

            turtle = next_turtle

    def part1(self):
        result = self.secret_message

        print("Part 1:", result)

    def part2(self):
        result = self.step_count

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2017D19("2017/19.txt")
    code.part1()
    code.part2()
