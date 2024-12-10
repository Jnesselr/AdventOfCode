from aoc.util.coordinate import Coordinate
from aoc.util.graph import Graph
from aoc.util.inputs import Input


class Y2024D10(object):
    def __init__(self, file_name):
        grid = Input(file_name).grid()

        def _can_walk(_from: str, _to: str) -> bool:
            return int(_to) - 1 == int(_from)

        graph = grid.to_graph(
            *'0123456789',
            test=_can_walk,
            directional=True
        )

        nine_coordinates = set(grid.find('9'))

        self._graphs: dict[Coordinate, Graph[Coordinate]] = {}  # Key is trailhead, value is sub graph
        self._nines: dict[Coordinate, set[Coordinate]] = {}  # Key is trailhead, value is trail end
        for zero_coordinate in grid.find('0'):
            self._graphs[zero_coordinate] = sub_graph = graph.subgraph(zero_coordinate)
            self._nines[zero_coordinate] = nine_coordinates.intersection(sub_graph.all_nodes)

    def part1(self):
        result = sum(len(nines) for nines in self._nines.values())

        print("Part 1:", result)

    def part2(self):
        result = sum(self._get_rating(zero) for zero in self._graphs.keys())

        print("Part 2:", result)

    def _get_rating(self, zero_coordinate: Coordinate) -> int:
        sub_graph = self._graphs[zero_coordinate]
        nines = self._nines[zero_coordinate]

        last_node_path = {
            frozenset({zero_coordinate}): zero_coordinate
        }

        result = 0

        while len(last_node_path) > 0:
            new_last_node_path = {}
            for path, last_node in last_node_path.items():
                if last_node in nines:
                    result += 1
                    continue

                new_nodes = sub_graph.nodes_from(last_node)
                for new_node in new_nodes:
                    new_last_node_path[frozenset(path.union({new_node}))] = new_node

            last_node_path = new_last_node_path

        return result


if __name__ == '__main__':
    code = Y2024D10("2024/10.txt")
    code.part1()
    code.part2()
