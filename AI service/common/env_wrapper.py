import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

from common.environment import make_env
from common.robot import Movement


class EnvWrapper(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    def __init__(self, config=None):
        self.viewer = None

        self.env = make_env(config=config)
        # raise AttributeError("One must supply either a maze_file path (str) or the maze_size (tuple of length 2)")

        self.env_size = self.env.size

        # all movements + wait action
        self.action_space = spaces.Discrete(4 * len(self.env_size) + 1)

        # observation is the x, y coordinate of the grid
        low = np.zeros(len(self.env_size), dtype=int)
        high = np.array(self.env_size, dtype=int) - np.ones(len(self.env_size), dtype=int)
        self.observation_space = spaces.Box(low, high, dtype=np.int64)

        # initial condition
        self.state = None
        self.steps_beyond_done = None
        self.done = False

        # Simulation related variables.
        self.seed()
        self.reset()

        # Just need to initialize the relevant attributes
        # self.configure()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.env.move_robot(action)
        reward, carrying, done = self.env.requirements.validate(self.env)  # check if pickup and dropoff is successfull

        self.state = np.append(self.env.robot_position(), carrying)

        info = {}

        return self.state, reward, done, info

    def reset(self):
        self.env.reset_robot()
        self.env.reset_objectives()
        self.state = np.zeros(2)
        self.steps_beyond_done = None
        self.done = False
        return np.append(self.env.robot.get_position(), 0)

    def render_state(self):
        return self.env


