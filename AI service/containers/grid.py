"""Object class for Grid manipulation and shortest path algorithm
"""

import collections
import numpy as np
from common.robot import Robot
from common.objectives import Objectives


class Grid(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, config=None):
        self._width = config["width"]
        self._height = config["height"]
        self._obstacle = '*'
        self._stored_positions = []

        self.grid = [[0 for x in range(self._width)] for y in range(self._height)]

        return

    def build_obstacles(self):
        return

    def bfs(self, grid, start, goal):
        queue = collections.deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[y][x] == goal:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < self._width and 0 <= y2 < self._height and grid[y2][x2] != self._obstacle and (
                        x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def update(self, robots: [Robot], pickup: Objectives, dropoff: Objectives):
        self.reset_grid()
        for i in robots:
            x, y = i.get_position()
            self._stored_positions.append((x, y))
            try:
                self.grid[x][y] = i
            except IndexError:
                print("{}, {}".format(x, y))

        for i in range(len(pickup.get_positions())):
            x,y = pickup.get_positions()[i]
            if self.grid[x][y] is not 0: # pickup is on a position of an agent
                self.grid[x][y].set_pickup(i, pickup)
            else:
                self._stored_positions.append((x, y))
                self.grid[x][y] = pickup

        for x, y in dropoff.get_positions():
            self._stored_positions.append((x, y))
            self.grid[x][y] = dropoff

    def reset_grid(self):
        for x, y in self._stored_positions:
            self.grid[x][y] = 0
