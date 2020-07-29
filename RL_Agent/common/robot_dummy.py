"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import random
from enum import Enum

from common.robot import Robot


class RobotDummy(Robot):

    # The class "constructor" - It's actually an initializer 
    def __init__(self, id, posX, posY, width, height, diameter, speed):
        super().__init__(id, posX, posY, width, height, diameter, speed)

    def move(self, action=-1):
        if action == -1:
            return super().move(random.randrange(5))
        return super().move(action)

    def isDummy(self):
        return True

    def get_position(self):
        return self.posY, self.posX

    def reset(self):
        self.posX = random.randint(0, self.width - 1)
        self.posY = random.randint(0, self.height - 1)
        self.rewarded = False