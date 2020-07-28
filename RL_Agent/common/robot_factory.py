"""Abstract Robot Factory
"""

from common.robot_agent import RobotAgent
from common.robot_dummy import RobotDummy


def make_agent(id, grid, width=100, height=100, diameter=20, speed=1):
    x, y = grid.calculate_random_pos()
    return RobotAgent(id, x, y, width, height, diameter, speed)


def make_dummy(id, grid, width=100, height=100, diameter=20, speed=1):
    x, y = grid.calculate_random_pos(agent=False, dummy_y=id)
    return RobotDummy(id, x, y, width, height, diameter, speed)
