"""Map class
"""

import math


class Map(object):
    width = 0
    height = 0
    map = []

    # The class "constructor" - It's actually an initializer
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.map = [0 for i in range(width * height)]

    def encode(self, x, y):
        return y * self.width + x

    def decode(self, num):
        return num % self.width, math.floor(num / self.width)

    def set_map(self, x, y, value):
        self.map[self.encode(x, y)] = value

    def get_map(self):
        return self.map
