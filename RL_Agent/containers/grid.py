"""Object class for Grid manipulation and shortest path algorithm
"""

from common.robot import Robot
import random
import math
import numpy as np


class Grid(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid=[], width= 0, height=0):
        self._stored_positions = []
        self._width = width
        self._height = height
        self.data = grid

    def update(self, robots: [Robot], obj_manager):
        self.reset_grid()
        for idx, i in robots.items():
            y, x = i.get_position()
            self._stored_positions.append((y, x))
            try:
                self.data[y][x].append(idx)
            except IndexError:
                print("{}, {}".format(x, y))

        for key, objective in obj_manager.get_objectives().items():
            # objective -> Objectives
            p_pos = objective.get_pickup_np()
            d_pos = objective.get_dropoff_np()
            y, x = p_pos[0], p_pos[1]
            y1, x1 = d_pos[0], d_pos[1]

            self._stored_positions.append((y, x))
            self.data[y][x].append("P" + str(key))

            self._stored_positions.append((y1, x1))
            self.data[y1][x1].append("D" + str(key))

    def get_sensoric_distance(self, pos):
        """
        computes the discrete distance of close-by objects around pos
        using loops and checking every direction
        :return: 8 sensoric distance numbers in a list
        """

        # order: north,south,west,east,nw,ne,sw,se
        sensor_list = [0, 0, 0, 0, 0, 0, 0, 0]
        tmp = np.arange(2)
        distance = 1
        while distance < 3:
            # check NORTH
            list_count = 0
            tmp[:] = pos
            tmp[0] = max(pos[0] - distance, 0)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check SOUTH
            list_count += 1
            tmp[:] = pos
            tmp[0] = min(pos[0] + distance, self._height - 1)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check WEST
            list_count += 1
            tmp[:] = pos
            tmp[1] = max(pos[1] - distance, 0)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check EAST
            list_count += 1
            tmp[:] = pos
            tmp[1] = min(pos[1] + distance, self._width - 1)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check NORTH WEST
            list_count += 1
            tmp[:] = pos
            tmp[0] = max(pos[0] - distance, 0)
            tmp[1] = max(pos[1] - distance, 0)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check NORTH EAST
            list_count += 1
            tmp[:] = pos
            tmp[0] = max(pos[0] - distance, 0)
            tmp[1] = min(pos[1] + distance, self._width - 1)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check SOUTH WEST
            list_count += 1
            tmp[:] = pos
            tmp[0] = min(pos[0] + distance, self._height - 1)
            tmp[1] = max(pos[1] - distance, 0)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            # check SOUTH EAST
            list_count += 1
            tmp[:] = pos
            tmp[0] = min(pos[0] + distance, self._height - 1)
            tmp[1] = min(pos[1] + distance, self._width - 1)
            if self.check_collision(tmp) and sensor_list[list_count] == 0:
                sensor_list[list_count] = distance

            distance += 1

        return sensor_list

    def check_pickup_delivery(self, agentID, obj_manager):
        """
        looks if agentPos in grid has pickup and dropoff object
        :return: Boolean value indicating if agent successfully dropped of the pickup target
        """
        get_obj = obj_manager.get_robot_objective_dict()
        if agentID not in get_obj:
            return False

        objective_id = get_obj[agentID]
        objective = obj_manager.get_objectives()[objective_id]
        return objective.is_delivered()

    def check_collision(self, pos):
        self.check_boundary(pos)

        # if agent collided with obstacles and if pickup collided with anything else
        agent_num = 0
        for i in self.data[pos[0]][pos[1]]:

            if is_number(i):
                agent_num += 1

            if i == '#' or agent_num > 1 or (not is_number(i) and i.startswith('P')):  # or i.startswith('X')
                return True

        return False

    def check_collision_into_solids(self, pos, carrying=False):
        # use this method to prevent the agent from moving into an obstacle
        self.check_boundary(pos)

        # if agent collided with obstacles and if pickup collided with anything else
        agent_num = 0
        for i in self.data[pos[0]][pos[1]]:
            if is_number(i):
                agent_num += 1

            if i == '#' or (not is_number(i) and i.startswith('P') and not carrying):  # or i.startswith('X')
                return True

        return False

    def check_boundary(self, pos):
        # Is used to prevent agents in running into walls
        # check boundaries
        if (pos[0] < 0 or pos[0] >= self._height) or (pos[1] < 0 or pos[1] >= self._width):
            return True
        return False

    def check_collision_as_pickup(self, pos):
        # if agent collided with obstacles and if pickup collided with anything else
        agent_num = 0
        for i in self.data[pos[0]][pos[1]]:

            if is_number(i):
                agent_num += 1

            if i == '#' or agent_num > 1:  # or i.startswith('X')
                return True

        return False

    def reset_grid(self):
        for y, x in self._stored_positions:
            if '#' in self.data[y][x]:
                self.data[y][x] = ['#']
            else:
                self.data[y][x] = []
        self._stored_positions = []

    def check_occupancy_free(self, x, y):
        return len(self.data[y][x]) == 0

    def calculate_random_pos(self):
        while True:
            x = math.floor((self._width - 1) * random.uniform(0.0, 1.0))
            y = math.floor((self._height - 1) * random.uniform(0.0, 1.0))
            if self.check_occupancy_free(x, y):
                break

        return x, y


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
