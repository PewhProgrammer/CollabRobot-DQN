"""Abstract Robot Factory
"""

from common.robot import Robot
from common.robot_agent import RobotAgent
from common.robot_dummy import RobotDummy
import random
import math


def make_agent(width=100, height=100, diameter=20, speed=1):
    x, y = calculate_random_pos(width, height)
    return RobotAgent(x, y, width, height, diameter, speed)


def make_dummy(width=100, height=100, diameter=20, speed=1):
    x, y = calculate_random_pos(width, height)
    return RobotDummy(x, y, width, height, diameter, speed)


def calculate_random_pos(width, height):
    x = math.floor((width - 1) * random.uniform(0.0, 1.0))
    y = math.floor((height - 1) * random.uniform(0.0, 1.0))
    return x, y
