"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import random
from enum import Enum


class Movement(Enum):
    WAIT = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    NORTH_WEST = 5
    NORTH_EAST = 6
    SOUTH_WEST = 7
    SOUTH_EAST = 8


class Robot(object):
    posX = 0
    posY = 0
    diam = 0
    speed = 0
    height = 0
    width = 0
    target = 0
    carrier = False

    # The class "constructor" - It's actually an initializer 
    def __init__(self, posX, posY, width, height, diameter, speed):
        self.posX = posX
        self.posY = posY
        self.diam = diameter
        self.speed = speed
        self.width = width
        self.height = height

    def wait(self):
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
        Movement.NORTH_WEST: north_west,
        Movement.NORTH_EAST: north_east,
        Movement.SOUTH_WEST: south_west,
        Movement.SOUTH_EAST: south_east
    }

    def move(self, num):
        self.options[num](self)
        return self.get_position()

    def get_position(self):
        return self.posX, self.posY

    def set_carrier(self, value):
        self.carrier = value

    def get_carrier(self):
        return self.carrier


def get_sample_movement():
    return Movement(random.randint(0, 8))