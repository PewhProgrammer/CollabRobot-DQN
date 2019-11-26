"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import math
import random

from common.robot import Robot, Movement, get_sample_movement
from common.robot_factory import make_robot
from common.map import Map
from logic.requirements import Requirements


class Environment(object):
    width = 0
    height = 0
    units = {}
    pickup = 0
    dropoff = 0
    map = None
    requirements = None

    # The class "constructor" - It's actually an initializer 
    def __init__(self, width, height, robots, pickupX, pickupY, dropoffX, dropoffY):
        self.width = width
        self.height = height
        self.units = robots
        self.map = Map(width, height)
        self.generate_objective(pickupX, pickupY, dropoffX, dropoffY)
        self.requirements = Requirements(self.pickup, self.dropoff)

    def generate_objective(self, pickupX=-1, pickupY=-1, dropoffX=-1, dropoffY=-1):
        # create new pickup and dropoff point
        x, y = self.generate_point(pickupX, pickupY)
        self.pickup = self.map.encode(x, y)

        x, y = self.generate_point(dropoffX, dropoffY)
        self.dropoff = self.map.encode(x, y)

    def generate_point(self, x, y):
        if x == -1:
            x = math.floor((self.width - 1) * random.uniform(0.0, 1.0))
        if y == -1:
            y = math.floor((self.height - 1) * random.uniform(0.0, 1.0))

        return x, y


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


def env_reset():
    make_env(env.width, env.height, config=cfg)
    return env


def get_movement(movementID, rID):
    return {rID: Movement(movementID)}


def update_map(agent, robotID):
    x, y = agent.get_position()
    # print("map: " + str(x) + ", " + str(y))
    env.map.set_map(x, y, robotID)


def make_env(width, height, count=1, config=None):
    global env, cfg
    robots = {}
    cfg = config

    if config is None:
        agent_posX, agent_posY, pickupX, pickupY, dropoffX, dropoffY = -1, -1, -1, -1, -1, -1
    else:
        agent_posX, agent_posY, pickupX, pickupY, dropoffX, dropoffY = [config["agentPosX"], config["agentPosY"],
                                                                        config["pickupX"], config["pickupY"],
                                                                        config["dropoffX"], config["dropoffY"]]

    for x in range(count):
        robot = make_robot(agent_posX, agent_posY, width=width, height=height, distributed=(agent_posX == -1))
        robots[x] = robot

    env = Environment(width, height, robots, pickupX, pickupY, dropoffX, dropoffY)


def get_env():
    return env
