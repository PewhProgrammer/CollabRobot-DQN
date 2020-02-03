"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import math
import random
import numpy as np

from common.robot_factory import make_agent, make_dummy
from logic.requirements import Requirements


class Environment(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            raise AttributeError(f'{self.__class__.__name__}.{config} config not given.')

        self.width = self.config["width"]
        self.height = self.config["height"]
        self.size = (self.width, self.height)

        self.robot = make_agent(width=self.width, height=self.height)
        self.robots = []
        self.robots.append(self.robot)  # agent always in #1

        self.last_action = None
        self.episode = -1

        for i in range(self.config["dummies"]):
            self.robots.append(make_dummy(width=self.width, height=self.height))

        self.generate_objective()
        self.requirements = Requirements(self.pickup, self.dropoff)

    def generate_objective(self):
        if self.config is None:
            pickupX, pickupY, dropoffX, dropoffY = -1, -1, -1, -1
        else:
            pickupX, pickupY, dropoffX, dropoffY = [self.config["pickupX"], self.config["pickupY"],
                                                    self.config["dropoffX"], self.config["dropoffY"]]

        # create new pickup and dropoff point
        self.pickup = self.generate_random_point(pickupX, pickupY)
        self.dropoff = self.generate_random_point(dropoffX, dropoffY)

    def generate_random_point(self, x, y) -> np.array:

        if x == -1:
            x = math.floor((self.width - 1) * random.uniform(0.0, 1.0))
        if y == -1:
            y = math.floor((self.height - 1) * random.uniform(0.0, 1.0))

        return np.array([x, y])

    def move_robots(self, action):
        # move the agent with the action and move the dummys with random action
        self.last_action = int(action)
        for r in self.robots:
            r.move(action)

    def robot_position(self) -> np.array:
        r = self.robot.get_position()
        return np.array([r[0], r[1]])

    def robot_positions(self):
        dict = []

        for r in self.robots:

            pos = r.get_position()
            dict.append(pos)

        return dict

    def reset(self):
        for r in self.robots:
            r.reset()
        self.generate_objective()
        # reset means new start of episode
        self.episode += 1

        return np.append(self.robot.get_position(), 0)