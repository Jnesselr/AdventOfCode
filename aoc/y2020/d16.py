import re
from dataclasses import dataclass
from functools import reduce
from typing import Dict

from aoc.util.inputs import Input


@dataclass
class Field(object):
    start_range_a: int
    end_range_a: int
    start_range_b: int
    end_range_b: int

    def is_valid(self, number):
        return self.start_range_a <= number <= self.end_range_a or \
               self.start_range_b <= number <= self.end_range_b


class Y2020D16(object):
    def __init__(self, file_name):
        groups = Input(file_name).grouped()

        self.fields = {}
        for line in groups[0]:
            matched = re.match(r'([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
            self.fields[matched.group(1)] = Field(
                start_range_a=int(matched.group(2)),
                end_range_a=int(matched.group(3)),
                start_range_b=int(matched.group(4)),
                end_range_b=int(matched.group(5))
            )

        self.my_ticket = [int(x) for x in groups[1][1].split(',')]

        self.nearby_tickets = []
        for line in groups[2][1:]:
            self.nearby_tickets.append([int(x) for x in line.split(',')])

    def part1(self):
        result = 0

        for ticket in self.nearby_tickets:
            for ticket_field in ticket:
                ticket_field_valid = False
                field: Field
                for field in self.fields.values():
                    ticket_field_valid |= field.is_valid(ticket_field)

                if not ticket_field_valid:
                    result += ticket_field

        print("Part 1:", result)

    def part2(self):
        valid_tickets = [x for x in self.nearby_tickets if self._is_valid_ticket(x)]
        valid_tickets.append(self.my_ticket)
        index_to_ticket_values: Dict[int, set] = {}

        ticket_length = len(self.my_ticket)

        for ticket in valid_tickets:
            for index in range(ticket_length):
                if index not in index_to_ticket_values:
                    index_to_ticket_values[index] = set()
                index_to_ticket_values[index].add(ticket[index])

        field_to_valid_indexes: Dict[str, set] = {}

        for index in range(ticket_length):
            for field_name, field in self.fields.items():
                if field_name not in field_to_valid_indexes:
                    field_to_valid_indexes[field_name] = set()

                if all(field.is_valid(x) for x in index_to_ticket_values[index]):
                    field_to_valid_indexes[field_name].add(index)

        field_to_index: Dict[str, int] = {}
        while len(field_to_valid_indexes) > 0:
            fields_with_one_possibility = [f for f, indexes in field_to_valid_indexes.items() if len(indexes) == 1]

            for field in fields_with_one_possibility:
                index = list(field_to_valid_indexes[field])[0]
                field_to_index[field] = index
                del field_to_valid_indexes[field]

                for indexes in field_to_valid_indexes.values():
                    indexes.remove(index)

        departure_fields = [x for f, x in field_to_index.items() if f.startswith("departure")]
        departure_values = [self.my_ticket[x] for x in departure_fields]
        result = reduce(lambda x, y: x*y, departure_values)

        print("Part 2:", result)

    def _is_valid_ticket(self, ticket):
        for ticket_field in ticket:
            ticket_field_valid = False
            field: Field
            for field in self.fields.values():
                ticket_field_valid |= field.is_valid(ticket_field)

            if not ticket_field_valid:
                return False
        return True


if __name__ == '__main__':
    code = Y2020D16("2020/16.txt")
    code.part1()
    code.part2()
