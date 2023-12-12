from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.graph import Graph
from aoc.util.grid import Grid
from aoc.util.inputs import Input


class Y2023D1(object):
    def __init__(self, file_name):
        self.input_grid = Input(file_name).grid()

    def part1(self):
        result = self._get_expansion_at_scale(2)

        print("Part 1:", result)

    def part2(self):
        result = self._get_expansion_at_scale(1000000)

        print("Part 2:", result)

    def _get_expansion_at_scale(self, scale: int) -> int:

        all_rows = set(range(self.input_grid.height))
        all_cols = set(range(self.input_grid.width))

        galaxy_coordinates = self.input_grid.find('#')
        galaxy_rows = set(g.y for g in galaxy_coordinates)
        galaxy_cols = set(g.x for g in galaxy_coordinates)

        empty_rows = all_rows.difference(galaxy_rows)
        empty_cols = all_cols.difference(galaxy_cols)

        offset_row_counter = 0
        row_map = {}
        for row in range(self.input_grid.height):
            row_map[row] = row + offset_row_counter
            if row in empty_rows:
                offset_row_counter += (scale - 1)

        offset_col_counter = 0
        col_map = {}
        for col in range(self.input_grid.height):
            col_map[col] = col + offset_col_counter
            if col in empty_cols:
                offset_col_counter += (scale - 1)

        universe_graph: Graph[Coordinate] = Graph(directional=False)

        existing_nodes = set()
        for galaxy_coord in galaxy_coordinates:
            new_x = col_map[galaxy_coord.x]
            new_y = row_map[galaxy_coord.y]
            new_coordinate = Coordinate(new_x, new_y, CoordinateSystem.X_RIGHT_Y_DOWN)

            for node in existing_nodes:
                universe_graph.add(node, new_coordinate, node.manhattan(new_coordinate))

            existing_nodes.add(new_coordinate)

        return sum(int(e.weight) for e in universe_graph.all_edges) // 2


if __name__ == '__main__':
    code = Y2023D1("2023/11.txt")
    code.part1()
    code.part2()
