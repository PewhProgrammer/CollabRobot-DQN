"""Object class for objectives creation. A objective can be classified as pickup or dropoff target
"""
# pickup and dropoff targets are able to occupy more than one unit in the environment

import random
import numpy as np
import math
from enum import Enum


class ObjectiveType(Enum):
    PICKUP = 0
    DROPOFF = 1


class Objectives(object):

    def __init__(self, p_pos, d_pos):
        self._positions = []
        self._pickup = p_pos  # tuple (y,x)
        self._dropoff = d_pos
        self._delivered = False
        self._delivery_reward = 30

    def add_point(self, x, y):
        self._positions.append((x, y))
        return True

    def get_single_position(self, id) -> np.array:
        r = self._positions[id]
        return np.array([r[0], r[1]])

    def get_positions_np(self) -> np.array:
        agents = self.get_single_position(0)
        for i in range(len(self._positions) - 1):
            agents = np.concatenate((agents, self.get_single_position(i + 1)))

        return agents

    def get_dropoff_np(self) -> np.array:
        r = self._dropoff
        return np.array([r[0], r[1]])

    def get_pickup_np(self) -> np.array:
        r = self._pickup
        return np.array([r[0], r[1]])

    def pickup_move(self, new_pos):
        if self._delivered:
            return

        self._pickup = new_pos

        if self._pickup == self._dropoff:
            self._delivered = True

    def is_delivered(self):
        return self._delivered

    def delivery_reward(self):
        if not self._delivered:
            return 0

        reward = self._delivery_reward  # just once, then remove it
        self._delivery_reward = 0
        return reward


def generate_objective(pickuplist, dropofflist):
    # create new pickup and dropoff point
    pickup = Objectives(ObjectiveType.PICKUP)
    dropoff = Objectives(ObjectiveType.DROPOFF)

    for x, y in pickuplist:
        pickup.add_point(x, y)

    for x, y in dropofflist:
        dropoff.add_point(x, y)

    return pickup, dropoff


def generate_random_point(self, x, y) -> np.array:
    if x == -1:
        x = math.floor((self.width - 1) * random.uniform(0.0, 1.0))
    if y == -1:
        y = math.floor((self.height - 1) * random.uniform(0.0, 1.0))

    return np.array([x, y])


if __name__ == "__main__":
    obj = Objectives((0, 0), (1, 1))
    obj.pickup_move((1, 1))

    print(obj.is_delivered())
