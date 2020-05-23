"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import random
from enum import Enum
import numpy as np


class Movement(Enum):
    WAIT = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    GRASP = 5


class Robot(object):

    # The class "constructor" - It's actually an initializer 
    def __init__(self, id, posX, posY, width, height, diameter, speed):
        self.posX = posX
        self.posY = posY
        self.diam = diameter
        self.speed = speed
        self.width = width
        self.height = height
        self.rewarded = False
        self.id = id
        self.oldPos = (posY, posX)

    def wait(self):
        return

    def grasp(self):
        return

    def north(self):
        if self.posY - 1 >= 0:
            self.posY -= 1

    def south(self):
        if self.posY + 1 < self.height:
            self.posY += 1

    def east(self):
        if self.posX + 1 < self.width:
            self.posX += 1

    def west(self):
        if self.posX - 1 >= 0:
            self.posX -= 1

    def north_west(self):
        self.north()
        self.west()

    def north_east(self):
        self.north()
        self.east()

    def south_west(self):
        self.south()
        self.west()

    def south_east(self):
        self.south()
        self.east()

    # map the inputs to the function blocks
    options = {
        Movement.WAIT: wait,
        Movement.NORTH: north,
        Movement.SOUTH: south,
        Movement.EAST: east,
        Movement.WEST: west,
        Movement.GRASP: grasp
    }

    def move(self, action):
        self.oldPos = self.get_position()
        if isinstance(action, Movement):
            self.options[action](self)
        else:
            self.options[Movement(action)](self)

        return self.get_position()

    def get_latest_move_diff(self):
        newPos = self.get_position()
        ydiff = newPos[0] - self.oldPos[0]
        xdiff = newPos[1] - self.oldPos[1]
        return ydiff, xdiff


    def get_id(self):
        return self.id

    def get_position(self):
        return self.posY, self.posX

    def reset(self):
        self.posX = random.randint(0, self.width - 1)
        self.posY = random.randint(0, self.height - 1)
        self.rewarded = False


def get_sample_movement():
    return Movement(random.randint(0, 5))
