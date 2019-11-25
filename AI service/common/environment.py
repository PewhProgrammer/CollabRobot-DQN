"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

from common.robot import Robot, Movement, get_sample_movement


class Environment(object):
    width = 0
    height = 0
    units = {}

    # The class "constructor" - It's actually an initializer 
    def __init__(self, width, height, robots):
        self.width = width
        self.height = height
        self.units = robots


def make_robot(x, y, diameter, speed):
    return Robot(x, y, diameter, speed)


env = None


def move_robot():
    for key, robot in env.units.items():
        robot.move(Movement.NORTH_EAST)
    return env


def action_space_sample():
    action_space = {}
    for key, value in env.units.items():
        movement = get_sample_movement()
        action_space[key] = movement

    return action_space


def step(action_space):
    for rID, movement in action_space.items():
        env.units[rID].move(movement)

    return env, 10, False


def make_env(width, height, count):
    global env
    robots = {}
    for x in range(count):
        robot = Robot(width, height, 20, 1)
        robots[x] = robot

    env = Environment(width, height, robots)


def get_env():
    return env
