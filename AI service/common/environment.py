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

        if config is None:
            agent_posX, agent_posY, pickupX, pickupY, dropoffX, dropoffY = -1, -1, -1, -1, -1, -1
        else:
            agent_posX, agent_posY, pickupX, pickupY, dropoffX, dropoffY = [config["agentPosX"], config["agentPosY"],
                                                                            config["pickupX"], config["pickupY"],
                                                                            config["dropoffX"], config["dropoffY"]]

        self.robot = make_robot(agent_posX, agent_posY, width=size[0], height=size[1], distributed=(agent_posX == -1))
        self.generate_objective(pickupX, pickupY, dropoffX, dropoffY)
        self.requirements = Requirements(self.pickup, self.dropoff)

    def generate_objective(self, pickupX=-1, pickupY=-1, dropoffX=-1, dropoffY=-1):
        # create new pickup and dropoff point
        x, y = self.generate_point(pickupX, pickupY)
        self.pickup = np.array([x, y])

        x, y = self.generate_point(dropoffX, dropoffY)
        self.dropoff = np.array([x, y])

    def generate_point(self, x, y):
        if x == -1:
            x = math.floor((self.width - 1) * random.uniform(0.0, 1.0))
        if y == -1:
            y = math.floor((self.height - 1) * random.uniform(0.0, 1.0))

        return x, y

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


def make_env(size):
    global env
    env = Environment(size=size)
    return env


def get_env():
    return env
