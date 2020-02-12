"""Object class for robot creation and manipulation. Board Model
"""
# 11 DIFFERENT ACTION in ACTION SPACE
# VERTICAL, HORIZONTAL, DIAGONAL MOVEMENT + PICKUP + DROPOFF

import math
import random
import numpy as np
import networkx as nx
from containers.grid import Grid
from common.objectives import generate_objective

from common.robot_factory import make_agent, make_dummy
from logic.requirements import Requirements


class Environment(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            raise AttributeError(f'{self.__class__.__name__}.{config} config not given.')

        self.config = config

        self.width = self.config["width"]
        self.height = self.config["height"]

        self.grid = Grid(config)

        self.robot = make_agent(width=self.width, height=self.height)
        self.robots = [self.robot]  # agent always in #1

        self.last_action = None
        self.episode = -1

        for i in range(self.config["dummies"]):
            self.robots.append(make_dummy(width=self.width, height=self.height))

        self.pickup, self.dropoff = generate_objective(config['pickup'][1], config['dropoff'][1])
        # TODO whole requirements function
        self.requirements = Requirements(self.pickup, self.dropoff)

        self.update_grid()

    def update_grid(self):
        self.grid.update(self.robots, self.pickup, self.dropoff)
        k = 2

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

    def reset(self, trial):
        for r in self.robots:
            r.reset()
        self.pickup, self.dropoff = generate_objective(self.config['pickup'][1], self.config['dropoff'][1])
        self.requirements = Requirements(self.pickup, self.dropoff)
        # reset means new start of episode
        self.episode = trial

        self.update_grid()
