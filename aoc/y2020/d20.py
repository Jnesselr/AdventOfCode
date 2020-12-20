from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from itertools import groupby
from typing import Callable, Set, Dict

from aoc.util.coordinate import Coordinate, CoordinateSystem
from aoc.util.grid import Grid
from aoc.util.inputs import Input


@dataclass(frozen=True)
class TileEdges(object):
    num: int
    left: int  # LSB == top
    right: int  # LSB == top
    top: int  # LSB == left
    bottom: int  # LSB == left
    grid_func: Callable[[Grid[str]], Grid[str]] = field(compare=False)

    @staticmethod
    def from_grid(tile_num, grid: Grid[str]) -> TileEdges:
        left = right = 0
        top = bottom = 0

        for i in range(10):
            left |= (1 << i) if grid[0, i] == '#' else 0
            right |= (1 << i) if grid[9, i] == '#' else 0
            top |= (1 << i) if grid[i, 0] == '#' else 0
            bottom |= (1 << i) if grid[i, 9] == '#' else 0

        def identity(g):
            return g.copy()

        return TileEdges(tile_num, left, right, top, bottom, identity)

    @staticmethod
    def reverse(edge):
        return int("{0:010b}".format(edge)[::-1], 2)

    @property
    def all_possible_edges(self):
        edges = {self.left, self.right, self.top, self.bottom}
        edges = edges.union(set([self.reverse(x) for x in edges]))
        return edges

    def all_combinations(self):
        result = set()
        result.add(self)
        result.add(self.rotate_right())
        result.add(self.rotate_right().rotate_right())
        result.add(self.rotate_right().rotate_right().rotate_right())
        result.add(self.flip_vertical())
        result.add(self.flip_vertical().rotate_right())
        result.add(self.flip_horizontal())
        result.add(self.flip_horizontal().rotate_right())
        return result

    def flip_vertical(self):
        return TileEdges(
            num=self.num,
            left=self.reverse(self.left),
            right=self.reverse(self.right),
            top=self.bottom,
            bottom=self.top,
            grid_func=lambda g: self.grid_func(g).flip_vertical()
        )

    def flip_horizontal(self):
        return TileEdges(
            num=self.num,
            left=self.right,
            right=self.left,
            top=self.reverse(self.top),
            bottom=self.reverse(self.bottom),
            grid_func=lambda g: self.grid_func(g).flip_horizontal()
        )

    def rotate_right(self):
        return TileEdges(
            num=self.num,
            left=self.bottom,
            right=self.top,
            top=self.reverse(self.left),
            bottom=self.reverse(self.right),
            grid_func=lambda g: self.grid_func(g).rotate_right()
        )


class Y2020D20(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()

        tile_edges: Dict[int, TileEdges] = {}
        tile_grids: Dict[int, Grid[str]] = {}
        for group in groups:
            tile_match = re.match(r'Tile (\d+):', group[0])
            tile_num = int(tile_match.group(1))
            tile_grid = Grid.from_str(group[1:])

            tile_edge = TileEdges.from_grid(tile_num, tile_grid)
            tile_edges[tile_num] = tile_edge
            tile_grids[tile_num] = tile_grid

        self.image_tiles = self._assemble_tiles(tile_edges)
        self.image = self._make_image(self.image_tiles, tile_grids)

    @staticmethod
    def _assemble_tiles(tile_edges):
        edges_from_top: Dict[int, Set[TileEdges]] = {}
        edges_from_left: Dict[int, Set[TileEdges]] = {}

        for tile in tile_edges.values():
            for combination in tile.all_combinations():
                edges_from_top.setdefault(combination.top, set()).add(combination)
                edges_from_left.setdefault(combination.left, set()).add(combination)

        corners = []
        tiles_with_free_edge = [list(tiles)[0] for tiles in edges_from_top.values() if len(tiles) == 1]
        for tile_num, elements in groupby(tiles_with_free_edge, lambda x: x.num):
            if len(list(elements)) == 4:
                corners.append(tile_num)

        if len(corners) != 4:
            raise ValueError("Couldn't find the 4 corners!")

        corner = tile_edges[corners[0]]

        # First, find edges the corner will need to match
        other_edges = set()
        for edge in corner.all_possible_edges:
            for tile in edges_from_top[edge]:
                if tile.num != corner.num:
                    other_edges = other_edges.union(tile.all_possible_edges)

        # Rotate it until it matches those edges in the orientation we want (corner is top left of image
        while not (corner.right in other_edges and corner.bottom in other_edges):
            corner = corner.rotate_right()

        size = int(math.sqrt(len(tile_edges)))
        grid: Grid[TileEdges] = Grid[TileEdges](size, size)
        grid[0, 0] = corner

        for row in range(grid.height):
            for col in range(grid.width):
                tile_num = grid[col, row]
                if tile_num is not None:
                    continue

                top_possibilities = set()
                if (top_tile := grid[col, row - 1]) is not None:
                    for option in edges_from_top[top_tile.bottom]:
                        if option.num != top_tile.num:
                            top_possibilities.add(option)

                left_possibilities = set()
                if (left_tile := grid[col - 1, row]) is not None:
                    for option in edges_from_left[left_tile.right]:
                        if option.num != left_tile.num:
                            left_possibilities.add(option)

                if len(left_possibilities) == 1 and len(top_possibilities) == 0:
                    grid[col, row] = list(left_possibilities)[0]
                elif len(left_possibilities) == 0 and len(top_possibilities) == 1:
                    grid[col, row] = list(top_possibilities)[0]
                elif len(left_possibilities) >= 1 and len(top_possibilities) >= 1:
                    intersection = left_possibilities.intersection(top_possibilities)
                    if len(intersection) == 1:
                        grid[col, row] = list(intersection)[0]
                    else:
                        raise ValueError("Not sure what to do!")

        return grid

    @staticmethod
    def _make_image(image_tiles: Grid[TileEdges], tile_grids: Dict[int, Grid[str]]) -> Grid[str]:
        image: Grid[str] = Grid[str](image_tiles.width * 8, image_tiles.height * 8)
        for row in range(image_tiles.height):
            for col in range(image_tiles.width):
                tile = image_tiles[col, row]
                original_grid = tile_grids[tile.num]
                sub_grid = tile.grid_func(original_grid)
                for i in range(1, 9):
                    for j in range(1, 9):
                        image[8 * col + i - 1, 8 * row + j - 1] = sub_grid[i, j]

        return image

    def part1(self):
        result = self.image_tiles[0, 0].num * \
            self.image_tiles[0, self.image_tiles.height-1].num * \
            self.image_tiles[self.image_tiles.width-1, 0].num * \
            self.image_tiles[self.image_tiles.width-1, self.image_tiles.height-1].num

        print("Part 1:", result)

    def part2(self):
        result = 0

        one_rotate = self.image.rotate_right()
        vertical_flip = self.image.flip_vertical()
        horizontal_flip = self.image.flip_horizontal()
        images = [
            self.image,
            one_rotate,
            one_rotate.rotate_right(),
            vertical_flip,
            vertical_flip.rotate_right(),
            horizontal_flip,
            horizontal_flip.rotate_right()
        ]

        for image in images:
            pixels = set(image.find('#'))
            non_monster_pixels = self._find_sea_monster(pixels)

            if len(non_monster_pixels) != len(pixels):
                result = len(non_monster_pixels)
                break

        print("Part 2:", result)

    @staticmethod
    def _find_sea_monster(all_pixels: Set[Coordinate]) -> Set[Coordinate]:
        sea_monster = [
            Coordinate(x, y, system=CoordinateSystem.X_RIGHT_Y_DOWN)
            for x, y in [
                (18, -1), (0, 0), (5, 0), (6, 0), (11, 0), (12, 0), (17, 0), (18, 0),
                (19, 0), (1, 1), (4, 1), (7, 1), (10, 1), (13, 1), (16, 1)
            ]
        ]
        monster_size = len(sea_monster)

        non_monster_pixels = all_pixels.copy()
        for pixel in all_pixels:
            test_monster = set(pixel + coordinate for coordinate in sea_monster)
            if len(test_monster.intersection(all_pixels)) == monster_size:
                for removable_pixel in test_monster:
                    non_monster_pixels.remove(removable_pixel)

        return non_monster_pixels


if __name__ == '__main__':
    code = Y2020D20("2020/20.txt")
    code.part1()
    code.part2()
