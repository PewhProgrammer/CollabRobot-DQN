"""Object class for robot creation and manipulation. Board Model
"""

import math
import numpy as np
from containers.objective_manager import Objective_Manager

from common.robot_factory import make_agent, make_dummy
from logic.reward_static import Reward_Static
from logic.reward_gradient import RewardGradient
from logic.reward_custom import RewardGradientCustom

from io_functions.map_reader import load_map
from containers.grid import Grid
from common.robot import Movement


class Environment(object):
    """MODEL: Environment describing global state information"""

    # The class "constructor" - It's actually an initializer
    def __init__(self, config={}):

        if config is not None:
            self.config = config
        else:
            raise AttributeError(f'{self.__class__.__name__}.{config} config not given.')

        self.config = config

        self.width: int = self.config["width"]
        self.height: int = self.config["height"]
        self.max_euc_dist = math.sqrt(pow(self.width, 2) + pow(self.height, 2))

        self.grid = None
        self.objective_manager = None
        self.reward_manager = None
        self.robots = {}  # agent always in #1

        self.last_action = None
        self.episode = -1

    def update_grid(self):
        self.grid.update(self.robots, self.objective_manager)

    def move_objectives(self, rID):  # if necessary
        self.objective_manager.perform_action(self.robots[0], self.grid)

    def move_robots(self, action, rID):
        agent = self.robots[rID]
        if self.config["dummies"] > 0:
            for i, dummy in self.robots.items():
                if str(i).startswith('H'):
                    pos = dummy.move()
                    if self.grid.check_collision_into_solids(pos):
                        dummy.reset_position()

        # move the agent with the action
        actionID = int(action)
        if actionID == Movement.GRASP.value:  # robot is grasping; check for objectives in close proximity
            self.objective_manager.check_grasping_objective(self.robots[rID])
        self.last_action = actionID
        pos = agent.move(actionID)
        if self.grid.check_collision_into_solids(pos, self.objective_manager.is_grasping_objective(self.robots[rID])):
            agent.reset_position()

    def robot_position(self, rID) -> np.array:
        r = self.robots[rID].get_position()
        return np.array([r[0], r[1]])

    def all_agents_position(self):
        agents = self.robot_position(0)
        for i, robot in self.robots.items():
            if self.robots[i].isDummy() or i == 0:
                continue
            agents = np.concatenate((agents, self.robot_position(i)))

        return agents

    def robot_positions(self):
        dict = []

        for _, r in self.robots.items():
            pos = r.get_position()
            dict.append(pos)

        return dict

    def reached_pickups(self):
        # used to log the data inside of game log
        result = []
        for _, agent in self.robots.items():
            result.append(agent.rewarded)

        return result

    def reset(self, trial):
        for _, r in self.robots.items():
            r.reset()

        map_version = self.episode % self.config["map"][1]  # change map
        if self.config["map"][1] > 1:
            path = "{}v{}.map".format(self.config["map"][0], map_version)
        else:
            path = self.config["map"][0]
        self.grid, objective_list = load_map(path, self.width, self.height)
        self.objective_manager = Objective_Manager(objective_list)
        if "reward" in self.config and self.config["reward"] == "gradient":
            self.reward_manager = RewardGradient(self.grid, self.config)
        elif "reward" in self.config and self.config["reward"] == "custom":
            self.reward_manager = RewardGradientCustom(self.grid, self.config)
        else:
            self.reward_manager = Reward_Static(self.grid)

        self.robots = {}

        for i in range(self.config["agents"]):
            self.robots[i] = make_agent(i, self.grid, width=self.width, height=self.height)

        for i in range(self.config["dummies"]):
            i += self.config["agents"]
            self.robots["H" + str(i)] = make_dummy(i, self.grid, width=self.width, height=self.height)

        # reset means new start of episode
        self.episode = trial

        self.update_grid()
