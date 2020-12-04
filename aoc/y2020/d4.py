from dataclasses import dataclass, field
from typing import Optional

from aoc.util.inputs import Input


@dataclass
class Passport(object):
    birth_year: Optional[int] = field(default=None)
    issue_year: Optional[int] = field(default=None)
    expiration_year: Optional[int] = field(default=None)
    height: Optional[str] = field(default=None)
    hair_color: Optional[str] = field(default=None)
    eye_color: Optional[str] = field(default=None)
    passport_id: Optional[str] = field(default=None)
    country_id: Optional[str] = field(default=None)

    @property
    def has_required_fields(self):
        return self.birth_year is not None and \
                    self.issue_year is not None and \
                    self.expiration_year is not None and \
                    self.height is not None and \
                    self.hair_color is not None and \
                    self.eye_color is not None and \
                    self.passport_id is not None

    @property
    def is_valid(self):
        if not self.has_required_fields:
            return False

        if self.birth_year < 1920 or self.birth_year > 2002:
            return False

        if self.issue_year < 2010 or self.issue_year > 2020:
            return False

        if self.expiration_year < 2020 or self.expiration_year > 2030:
            return False

        if len(self.height) < 3:
            return False

        if self.height[-2:] == 'cm':
            value = int(self.height[0:-2])
            if value < 150 or value > 193:
                return False
        elif self.height[-2:] == 'in':
            value = int(self.height[0:-2])
            if value < 59 or value > 76:
                return False
        else:
            return False

        if len(self.hair_color) != 7 or self.hair_color[0] != '#':
            return False

        for character in self.hair_color[1:]:
            if character.isalpha():
                if not character.islower():
                    return False
                if character > 'f':
                    return False
            elif not character.isnumeric():
                return False

        if self.eye_color not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False

        if len(self.passport_id) != 9:
            return False

        return True


class Y2020D4(object):
    def __init__(self, file_name):
        lines = Input(file_name).lines()
        self.passports = []
        current_passport = Passport()

        for line in lines:
            if line == "":
                self.passports.append(current_passport)
                current_passport = Passport()
                continue

            segments = line.split(' ')
            for element in segments:
                key, value = element.split(':')

                if key == 'byr':
                    current_passport.birth_year = int(value)
                elif key == 'iyr':
                    current_passport.issue_year = int(value)
                elif key == 'eyr':
                    current_passport.expiration_year = int(value)
                elif key == 'hgt':
                    current_passport.height = value
                elif key == 'hcl':
                    current_passport.hair_color = value
                elif key == 'ecl':
                    current_passport.eye_color = value
                elif key == 'pid':
                    current_passport.passport_id = value
                elif key == 'cid':
                    current_passport.country_id = value

        self.passports.append(current_passport)

    def part1(self):
        result = len([1 for passport in self.passports if passport.has_required_fields])

        print("Part 1:", result)

    def part2(self):
        result = len([1 for passport in self.passports if passport.is_valid])

        print("Part 2:", result)


if __name__ == '__main__':
    code = Y2020D4("2020/4.txt")
    code.part1()
    code.part2()
