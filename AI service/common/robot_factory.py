"""Abstract Robot Factory
"""

from common.robot import Robot
import random
import math


def make_robot(width=100, height=100, diameter=20, speed=1):
    x = math.floor((width-1) * random.uniform(0.0, 1.0))
    y = math.floor((height-1) * random.uniform(0.0, 1.0))
    return Robot(x, y, width, height, diameter, speed)
