"""Object class for robot creation and manipulation. Board Model
"""

import math
import random
import numpy as np
import networkx as nx
from containers.grid import Grid
from containers.objective_manager import Objective_Manager
from common.objectives import generate_objective

from common.robot_factory import make_agent, make_dummy
from logic.requirements import Requirements

from io_functions.map_reader import load_map


class Environment(object):
    """MODEL: Environment describing global state information"""

    # The class "constructor" - It's actually an initializer
    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            raise AttributeError(f'{self.__class__.__name__}.{config} config not given.')

        self.config = config

        self.width = self.config["width"]
        self.height = self.config["height"]

        self.grid = None
        self.objective_manager = None
        self.requirements = None
        self.robots = {}  # agent always in #1

        self.last_action = None
        self.episode = -1

    def update_grid(self):
        self.grid.update(self.robots, self.objective_manager)

    def move_objectives(self, rID):  # if necessary
        self.objective_manager.perform_action(self.robots[0], self.grid)

    def move_robots(self, action, rID):
        # move the agent with the action
        actionID = int(action)
        if actionID == 5:  # robot is grasping; check for objectives in close proximity
            self.objective_manager.check_grasping_objective(self.robots[rID])
        self.last_action = actionID
        self.robots[rID].move(actionID)

    def robot_position(self, rID) -> np.array:
        r = self.robots[rID].get_position()
        return np.array([r[0], r[1]])

    def all_agents_position(self):
        agents = self.robot_position(0)
        for i in range(len(self.robots) - 1):
            agents = np.concatenate( (agents, self.robot_position(i+1)) )

        return agents

    def robot_positions(self):
        dict = []

        for _, r in self.robots.items():
            pos = r.get_position()
            dict.append(pos)

        return dict

    def reset(self, trial):
        for _, r in self.robots.items():
            r.reset()

        loaded_map, objective_list = load_map(self.config["map"], self.width, self.height)
        self.grid = Grid(loaded_map, self.config)
        self.objective_manager = Objective_Manager(objective_list)
        self.requirements = Requirements(self.grid)

        self.robots = {}

        for i in range(self.config["agents"]):
            self.robots[i] = make_agent(i, self.grid, width=self.width, height=self.height)

        for i in range(self.config["dummies"]):
            self.robots["H" + str(i)] = make_dummy(self.grid, width=self.width, height=self.height)

        # reset means new start of episode
        self.episode = trial

        self.update_grid()
