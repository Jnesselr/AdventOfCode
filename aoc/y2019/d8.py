from aoc.util.inputs import Input


class Layer(object):
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def count(self, pixel):
        return self.data.count(pixel)

    def view_through(self, layer):
        result_data = ""

        for top, bottom in zip(layer.data, self.data):
            if top == '2':
                result_data += bottom
            else:
                result_data += top

        return Layer(self.width, self.height, result_data)

    def print(self):
        for row in range(self.height):
            line = ""
            for col in range(self.width):
                index = row * self.width + col
                if self.data[index] == '1':
                    line += '#'
                else:
                    line += ' '
            print(line)


class Y2019D8(object):
    _width = 25
    _height = 6

    def __init__(self, file_name):
        line = Input(file_name).line()

        self.layers = []
        layer_size = self._width * self._height
        for i in range(0, len(line), layer_size):
            self.layers.append(Layer(self._width, self._height, line[i: i + layer_size]))

    def part1(self):
        num_zeros = self._width * self._height
        result = 0

        for layer in self.layers:
            num_zeros_in_layer = layer.count('0')
            if num_zeros_in_layer < num_zeros:
                num_zeros = num_zeros_in_layer
                result = layer.count('1') * layer.count('2')

        print("Part 1:", result)

    def part2(self):
        result = self.layers[0]

        for layer in self.layers:
            result = layer.view_through(result)

        print("Part 2:")
        result.print()


if __name__ == '__main__':
    code = Y2019D8("2019/8.txt")
    code.part1()
    code.part2()
