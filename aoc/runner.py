import importlib

from aoc.util.inputs import Input


class AoCRunner(object):
    years = [2015, 2016, 2017, 2018, 2019]
    
    def run(self):
        for year in self.years:
            self._run_year(year)

    def _run_year(self, year):
        print(f"=== Year {year} ===")
        for day in range(1, 26):
            self._run_day(year, day)
            print()

    def _run_day(self, year, day):
        print(f"=== Day {day} ===")
        module_name = f"aoc.y{year}.d{day}"
        class_name = f"Y{year}D{day}"
        file_name = f"{year}/{day}.txt"

        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"Module \"{module_name}\" not found")
            return

        if class_name not in module.__dict__:
            print(f"Class \"{class_name}\" not found")
            return

        if not Input(file_name).exists():
            print(f"File \"{file_name}\" does not exist")
            return

        cls = module.__dict__[class_name](file_name)
        cls.part1()
        cls.part2()


if __name__ == '__main__':
    runner = AoCRunner()
    runner.run()