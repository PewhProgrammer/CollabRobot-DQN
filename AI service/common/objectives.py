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

    def __init__(self, t: ObjectiveType = None):
        self._positions = []
        self._type = t

    def add_point(self, x, y):
        self._positions.append((x, y))
        return True

    def get_positions(self):
        return self._positions

    def move_position(self, idx, movePos: ()):
        # check if possible to move the pickup
        if self._type == ObjectiveType.DROPOFF:
            return False

        # check if pickup pieces are in reach
        for occupied in self._positions:
            # TODO: atm only works with 2 pickups
            if occupied[0] == movePos[0] and occupied[1] == movePos[1]:
                return False  # pickup would be moved onto another pickup spot

            if abs(occupied[0] - movePos[0]) > 1 or abs(occupied[1] - movePos[1]):
                return False  # x,y-coordinate is too far apart

        self._positions[idx] = movePos
        return True


def generate_objective(pickuplist, dropofflist):
    # create new pickup and dropoff point
    # return self.generate_random_point(pickupX, pickupY), self.generate_random_point(dropoffX, dropoffY)
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
