"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import random
from enum import Enum

from common.robot import Robot


class RobotDummy(Robot):

    # The class "constructor" - It's actually an initializer 
    def __init__(self, posX, posY, width, height, diameter, speed):
        super().__init__(posX, posY, width, height, diameter, speed)

    def move(self, action):
        return super().move(random.randrange(8))
