import gym
import numpy as np

from gym import spaces

from containers.environment import Environment


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, config=None, ep_length: int = 50):
        super(CustomEnv, self).__init__()

        self.config = config
        self.config["agents"] = 1
        ep_length = config["ep_length"]
        self.env = Environment(config=config)
        self.env_size = (config["width"], config["height"])

        # Define action and observation space
        # They must be gym.spaces objects

        self.N_DISCRETE_ACTIONS = 5
        if config["sensor_information"]:
            self.N_DISCRETE_OBSERVATION = config["observation_space"] + 8
        else:
            self.N_DISCRETE_OBSERVATION = config["observation_space"]
        # shape = shape.reshape(1, self.N_DISCRETE_OBSERVATION)

        # Example when using discrete actions:
        self.action_space = spaces.Discrete(self.N_DISCRETE_ACTIONS)
        # observation is the x, y coordinate of the grid
        self.observation_space = spaces.Box(low=0, high=100, shape=(1, self.N_DISCRETE_OBSERVATION), dtype=np.float16)

        # initial condition
        self.steps_beyond_done = None
        self.done = False
        self.successes = 0

        self.ep_length = ep_length
        self.current_step = 0
        self.num_resets = -1  # Becomes 0 after __init__ exits.

        # Simulation related variables.
        self.seed()
        self.reset()

    def step(self, action):

        agent = self.env.robots[0]

        self.env.move_robots(action, 0)
        self.env.move_objectives(0)
        self.env.update_grid()
        reward, done = self.env.reward_manager.observe(self.env, agent,
                                                       action)  # check if pickup and dropoff is successful

        info = {}
        if done:
            self.successes += 1
            info["is_success"] = 1
        elif self.current_step >= self.ep_length:
            info["is_success"] = 0

        if done or self.current_step >= self.ep_length:
            if agent.is_collided():
                info["is_collision"] = 1
            else:
                info["is_collision"] = 0

        done = self.current_step >= self.ep_length or done

        # determine data for input layer
        self.state = self.input_data(0)

        self.current_step += 1

        return self.state, reward, done, info

    def reset(self):
        self.current_step = 0
        self.num_resets += 1
        self.steps_beyond_done = None
        self.done = False
        self.env.reset(self.num_resets)
        self.state = self.input_data(0)

        return self.state  # reward, done, info can't be included

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    # scheme: agent pos, pickup pos, dropoff pos, carrying

    def input_data(self, robotID):

        data = self.env.all_agents_position(), \
               self.env.objective_manager.pickup_get_positions_np(), \
               self.env.objective_manager.dropoff_get_positions_np(), \
               self.env.objective_manager.has_pickup(robotID)

        if self.config["sensor_information"]:
            tmp = list(data) + self.env.grid.get_sensoric_distance(self.env.robot_position(robotID))
            data = tuple(tmp)

        shape = np.concatenate(data, axis=None)
        return shape.reshape(1, self.N_DISCRETE_OBSERVATION)

    def _observation_state(self):
        data = self.env.objective_manager.pickup_get_positions()

        return data

    def get_env(self):
        return self.env

    def get_episode_len(self):
        return self.ep_length