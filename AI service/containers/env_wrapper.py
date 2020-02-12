import numpy as np

import gym
from gym import spaces
from gym.utils import seeding

from containers.environment import Environment


class EnvWrapper(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    def __init__(self, config=None):
        self.viewer = None

        self.env = Environment(config=config)
        # raise AttributeError("One must supply either a maze_file path (str) or the maze_size (tuple of length 2)")

        self.env_size = (config["width"], config["height"])

        # all movements + wait action
        self.action_space = spaces.Discrete(4 * len(self.env_size) + 1)

        # observation is the x, y coordinate of the grid
        low = np.zeros(len(self.env_size), dtype=int)
        high = np.array(self.env_size, dtype=int) - np.ones(len(self.env_size), dtype=int)
        self.observation_space = 7

        # initial condition
        self.steps_beyond_done = None
        self.done = False

        # Simulation related variables.
        self.seed()

        # Just need to initialize the relevant attributes
        # self.configure()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.env.move_robots(action)
        reward, carrying, done = self.env.requirements.validate(self.env)  # check if pickup and dropoff is successful

        self.env.update_grid()

        # determine data for input layer
        state = self.input_data(carrying)

        info = {}

        return state, reward, done, info

    # scheme: agent pos, pickup pos, dropoff pos, carrying
    def input_data(self, c):
        shape = np.concatenate((self.env.robot_position(), self.env.pickup.get_positions()[0], self.env.dropoff.get_positions()[0], c), axis=None)
        return shape.reshape(1, self.observation_space)

    def reset(self, trial):
        self.steps_beyond_done = None
        self.done = False
        self.env.reset(trial)
        return self.input_data(False)

    def get_env(self):
        return self.env



