"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import random
from enum import Enum


class Movement(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    GRASP = 4

    def __init__(self, n=0, s=1, e=2, w=3, g=4):
        self.NORTH = n
        self.SOUTH = s
        self.EAST = e
        self.WEST = w
        self.GRASP = g


class Robot(object):

    # The class "constructor" - It's actually an initializer 
    def __init__(self, id=-1, posX=-1, posY=-1, width=0, height=0, diameter=0, speed=1):
        self.posX = posX
        self.posY = posY
        self.diam = diameter
        self.speed: int = speed
        self.width: int = width
        self.height = height
        self.rewarded = False
        self.id = id
        self.oldPos = (posY, posX)
        self.collided = False

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

    def set_collided(self, b):
        self.collided = b

    def is_collided(self):
        return self.collided

    def get_id(self):
        return self.id

    def get_position(self):
        return self.posY, self.posX

    def is_stuck(self, actionid):
        # check if previous action changed position or did not
        return self.posY == self.oldPos[0] and self.posX == self.oldPos[1] and actionid != Movement.GRASP.value

    def reset_position(self):
        self.posX, self.posY = self.oldPos[1], self.oldPos[0]

    def reset(self):
        self.posX = random.randint(0, self.width - 1)
        self.posY = random.randint(0, self.height - 1)
        self.oldPos = (self.posY, self.posX)
        self.rewarded = False
        self.collided = False

    def isDummy(self):
        return False


def get_sample_movement():
    return Movement(random.randint(0, 4))
