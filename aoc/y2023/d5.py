from dataclasses import dataclass
from typing import List, Optional

from tqdm import tqdm

from aoc.util.inputs import Input


@dataclass
class Range:
    start: int
    length: int


@dataclass(frozen=True)
class RangeMap:
    destination_start: int
    source_start: int
    length: int

    def __contains__(self, item: int) -> bool:
        return self.source_start <= item < self.source_start + self.length

    def __getitem__(self, item: int) -> Optional[int]:
        if item not in self:
            return None

        return self.destination_start + (item - self.source_start)

    def overlaps(self, r: Range) -> bool:
        # range start is between source start and source end
        if self.source_start <= r.start < self.source_start + self.length:
            return True

        # source start is between range start and range end
        if r.start <= self.source_start < r.start + r.length:
            return True

        return False


class Mapping:
    def __init__(self):
        self._mappings: List[RangeMap] = []

    def add(self, range_map: RangeMap):
        self._mappings.append(range_map)
        self._mappings = sorted(self._mappings, key=lambda m: m.source_start)

    def __getitem__(self, item: int) -> int:
        for mapping in self._mappings:
            if item in mapping:
                return mapping[item]

        return item

    def chop(self, *ranges: Range):
        # Each range can be handled independently
        result = []
        for current_range in ranges:
            for r in self._chop(current_range):
                result.append(r)

        return result

    def _chop(self, current_range: Range):
        overlapping = [m for m in self._mappings if m.overlaps(current_range)]
        overlapping = sorted(overlapping, key=lambda m: m.source_start)

        current_index = current_range.start
        end_index = current_index + current_range.length - 1

        for overlap in overlapping:
            # Handle the range before our first overlap
            if current_index < overlap.source_start:
                yield Range(
                    start=current_index,  # No need to remap this
                    length=overlap.source_start - current_index
                )
                current_index = overlap.source_start

            overlap_end_index = overlap.source_start + overlap.length - 1
            next_end_index = min(overlap_end_index, end_index)

            # We take what we can of the overlap
            yield Range(
                start=overlap[current_index],
                length=next_end_index - current_index + 1
            )
            current_index = next_end_index + 1  # + 1 because we want to start after where we just ended

        if current_index <= end_index:
            yield Range(
                start=current_index,  # No need to remap this
                length=end_index - current_index + 1
            )


class Y2023D5(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()

        self.seeds: List[int] = []
        self.seed_to_soil_map: Mapping = Mapping()
        self.soil_to_fertilizer_map: Mapping = Mapping()
        self.fertilizer_to_water_map: Mapping = Mapping()
        self.water_to_light_map: Mapping = Mapping()
        self.light_to_temperature_map: Mapping = Mapping()
        self.temperature_to_humidity_map: Mapping = Mapping()
        self.humidity_to_location_map: Mapping = Mapping()

        for group in groups:
            first_line = group[0]
            if first_line.startswith('seeds: '):
                self.seeds = [int(x) for x in first_line[7:].split(' ')]
            elif first_line.startswith('seed-to-soil map:'):
                self._fill_in_mappings(self.seed_to_soil_map, group)
            elif first_line.startswith('soil-to-fertilizer map:'):
                self._fill_in_mappings(self.soil_to_fertilizer_map, group)
            elif first_line.startswith('fertilizer-to-water map:'):
                self._fill_in_mappings(self.fertilizer_to_water_map, group)
            elif first_line.startswith('water-to-light map:'):
                self._fill_in_mappings(self.water_to_light_map, group)
            elif first_line.startswith('light-to-temperature map:'):
                self._fill_in_mappings(self.light_to_temperature_map, group)
            elif first_line.startswith('temperature-to-humidity map:'):
                self._fill_in_mappings(self.temperature_to_humidity_map, group)
            elif first_line.startswith('humidity-to-location map:'):
                self._fill_in_mappings(self.humidity_to_location_map, group)
            else:
                raise Exception("Unknown grouping!")

    @staticmethod
    def _fill_in_mappings(mapping: Mapping, group: List[str]) -> None:
        for line in group[1:]:
            destination_start, source_start, length = line.split(' ')
            mapping.add(RangeMap(
                destination_start=int(destination_start),
                source_start=int(source_start),
                length=int(length)
            ))

    def part1(self):
        result = None

        for seed in self.seeds:
            seed_range = Range(start=seed, length=1)
            min_location = self._get_min_location(seed_range)

            result = min_location if result is None else min(result, min_location)

        print("Part 1:", result)

    def part2(self):
        result = None

        for i in range(0, len(self.seeds), 2):
            seed_start, length = self.seeds[i:i + 2]
            seed_range = Range(start=seed_start, length=length)
            min_location = self._get_min_location(seed_range)

            result = min_location if result is None else min(result, min_location)

        print("Part 2:", result)

    def _get_min_location(self, seed_range):
        soil = self.seed_to_soil_map.chop(seed_range)
        fertilizer = self.soil_to_fertilizer_map.chop(*soil)
        water = self.fertilizer_to_water_map.chop(*fertilizer)
        light = self.water_to_light_map.chop(*water)
        temperature = self.light_to_temperature_map.chop(*light)
        humidity = self.temperature_to_humidity_map.chop(*temperature)
        location = self.humidity_to_location_map.chop(*humidity)
        min_location = min(l.start for l in location)

        return min_location


if __name__ == '__main__':
    code = Y2023D5("2023/5.txt")
    code.part1()
    code.part2()
