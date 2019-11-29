"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import math
import random
import numpy as np

from common.robot import Robot, Movement, get_sample_movement
from common.robot_factory import make_robot
from common.map import Map
from logic.requirements import Requirements


class Environment(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, size, config=None):
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.map = Map(self.width, self.height)
        self.config = config

        self.robot = make_robot(width=size[0], height=size[1])
        self.generate_objective()
        self.requirements = Requirements(self.pickup, self.dropoff)

    def generate_objective(self):
        if self.config is None:
            pickupX, pickupY, dropoffX, dropoffY = -1, -1, -1, -1
        else:
            pickupX, pickupY, dropoffX, dropoffY = [self.config["pickupX"], self.config["pickupY"],
                                                    self.config["dropoffX"], self.config["dropoffY"]]

        # create new pickup and dropoff point
        self.pickup = self.generate_point(pickupX, pickupY)
        self.dropoff = self.generate_point(dropoffX, dropoffY)

    def generate_point(self, x, y) -> np.array:

        if x == -1:
            x = math.floor((self.width - 1) * random.uniform(0.0, 1.0))
        if y == -1:
            y = math.floor((self.height - 1) * random.uniform(0.0, 1.0))

        return np.array([x, y])

    def move_robot(self, action):
        self.robot.move(action)

    def robot_position(self) -> np.array:
        r = self.robot.get_position()
        return np.array([r[0], r[1]])

    def pickup_position(self) -> np.array:
        return self.pickup

    def dropoff_position(self) -> np.array:
        return self.dropoff

    def reset_robot(self):
        self.robot.reset()

    def reset_objectives(self):
        self.generate_objective()


env = None
cfg = {}


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
    done = False
    state, reward = -1, -1
    map = env.map

    for rID, movement in action_space.items():
        agent = env.units[rID]
        update_map(agent, 0)  # empty agent cell

        x, y = agent.move(movement)
        state = map.encode(x, y)
        update_map(agent, rID)  # update agent cell with new position

        reward, done = env.requirements.validate(agent, map, env)  # check if pickup and dropoff is successfull

    return state, reward, done, env


def calc_state():
    pos_x, pos_y = env.units[0].get_position()
    return env.map.encode(pos_x, pos_y)


def get_movement(movementID, rID):
    return {rID: Movement(movementID)}


def update_map(agent, robotID):
    x, y = agent.get_position()
    # print("map: " + str(x) + ", " + str(y))
    env.map.set_map(x, y, robotID)


def make_env(size, config=None):
    global env
    env = Environment(size=size, config=config)
    return env


def get_env():
    return env
