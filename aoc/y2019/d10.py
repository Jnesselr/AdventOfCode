import math
from math import gcd

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2019D10(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()

        self.grid: Grid[str] = Grid.from_str(lines)

        self.asteroids = self.grid.find('#')
        self.monitoring_station = None

        most_asteroids = 0
        for asteroid in self.asteroids:
            asteroid_visible_count = len(self._asteroids_visible_from(asteroid))
            if asteroid_visible_count > most_asteroids:
                most_asteroids = asteroid_visible_count
                self.monitoring_station = asteroid

    def part1(self):
        result = len(self._asteroids_visible_from(self.monitoring_station))

        print("Part 1:", result)

    def part2(self):
        result = None
        count = 0

        while result is None and len(self.asteroids) > 0:
            visible_asteroids = self._asteroids_visible_from(self.monitoring_station)
            visible_asteroids = sorted(visible_asteroids, key=lambda x: self._get_angle_for_position(x))

            for asteroid in visible_asteroids:
                self.grid[asteroid] = '.'
                self.asteroids.remove(asteroid)
                count += 1

                if count == 200:
                    result = asteroid.x * 100 + asteroid.y
                    break

        print("Part 2:", result)

    def _get_angle_for_position(self, asteroid: Coordinate) -> float:
        d_x = asteroid.x - self.monitoring_station.x
        d_y = asteroid.y - self.monitoring_station.y
        angle = math.degrees(math.atan2(d_y, d_x)) + 90.0

        if angle < 0:
            angle += 360.0

        return angle


    def _asteroids_visible_from(self, base: Coordinate):
        seen_angles = {}

        asteroid: Coordinate
        for asteroid in self.asteroids:
            dx = asteroid.x - base.x
            dy = asteroid.y - base.y

            if dx == dy == 0:
                continue

            divider = gcd(dx, dy)
            dx = dx // divider
            dy = dy // divider
            t = (dx, dy,)

            # Asteroid is closer than what we have
            if t in seen_angles and seen_angles[t] > divider:
                seen_angles[t] = divider
            elif t not in seen_angles:
                seen_angles[t] = divider

        result = []
        for position, divider in seen_angles.items():
            coordinate = Coordinate(
                position[0] * divider + base.x,
                position[1] * divider + base.y,
                system=CoordinateSystem.X_RIGHT_Y_DOWN
            )
            result.append(coordinate)

        return result


if __name__ == '__main__':
    code = Y2019D10("2019/10.txt")
    code.part1()
    code.part2()
