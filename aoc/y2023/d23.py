from aoc.util.coordinate import Coordinate
from aoc.util.graph import Graph, CompressionWhatToKeep
from aoc.util.inputs import Input


class Y2023D23(object):
    def __init__(self, file_name):
        grid = Input(file_name).grid()

        walkable = ['.', '>', '<', '^', 'v']
        self.icy_hike: Graph[Coordinate] = grid.to_graph(*walkable, directional=True)
        self.horrible_hike: Graph[Coordinate] = grid.to_graph(*walkable)

        # We can only go downhill, so we rip up any uphill paths
        for coordinate in grid.find('>'):
            before = coordinate.left()
            after = coordinate.right()
            self.icy_hike.remove_node_link(after, coordinate)
            self.icy_hike.remove_node_link(coordinate, before)

        for coordinate in grid.find('<'):
            before = coordinate.right()
            after = coordinate.left()
            self.icy_hike.remove_node_link(after, coordinate)
            self.icy_hike.remove_node_link(coordinate, before)

        for coordinate in grid.find('^'):
            before = coordinate.down()
            after = coordinate.up()
            self.icy_hike.remove_node_link(after, coordinate)
            self.icy_hike.remove_node_link(coordinate, before)

        for coordinate in grid.find('v'):
            before = coordinate.up()
            after = coordinate.down()
            self.icy_hike.remove_node_link(after, coordinate)
            self.icy_hike.remove_node_link(coordinate, before)

        all_valid_walkable = grid.find(lambda i: i in walkable)
        self.start = [c for c in all_valid_walkable if c.y == 0][0]
        self.end = [c for c in all_valid_walkable if c.y == grid.height - 1][0]

        # Let's simplify our graph. We only care about a point if we have 3 ways to get to it (or start/end)
        we_care_about_you: set[Coordinate] = {self.start, self.end}
        for coordinate in all_valid_walkable:
            if sum(grid[n] in walkable for n in coordinate.neighbors()) > 2:
                we_care_about_you.add(coordinate)

        self.icy_hike.compress(*we_care_about_you, keep_logic=CompressionWhatToKeep.ALL)
        self.horrible_hike.compress(*we_care_about_you, keep_logic=CompressionWhatToKeep.ALL)

    def part1(self):
        result = self.icy_hike.get_weight(self.icy_hike.flood_find_max(self.start, self.end))

        print("Part 1:", result)

    def part2(self):
        result = self.horrible_hike.get_weight(self.horrible_hike.flood_find_max(self.start, self.end))

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2023D23("2023/23.txt")
    code.part1()
    code.part2()
