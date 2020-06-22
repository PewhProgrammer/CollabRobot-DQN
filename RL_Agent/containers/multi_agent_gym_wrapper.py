import gym
import numpy as np

from gym import spaces

from containers.environment import Environment


class MultiAgentCustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, config=None, model_trained=None, ep_length: int = 100):
        super(MultiAgentCustomEnv, self).__init__()

        self.model_trained = model_trained
        self.env = Environment(config=config)
        # raise AttributeError("One must supply either a maze_file path (str) or the maze_size (tuple of length 2)")

        self.env_size = (config["width"], config["height"])

        # Define action and observation space
        # They must be gym.spaces objects

        self.N_DISCRETE_ACTIONS = 6
        self.N_DISCRETE_OBSERVATION = config["observation_space"]
        # shape = shape.reshape(1, self.N_DISCRETE_OBSERVATION)

        # Example when using discrete actions:
        self.action_space = spaces.Discrete(self.N_DISCRETE_ACTIONS)
        # observation is the x, y coordinate of the grid
        self.observation_space = spaces.Box(low=0, high=100, shape=(1, self.N_DISCRETE_OBSERVATION), dtype=np.float16)

        # initial condition
        self.steps_beyond_done = None
        self.done = False

        self.ep_length = ep_length
        self.current_step = 0
        self.num_resets = -1  # Becomes 0 after __init__ exits.

        # Simulation related variables.
        self.seed()
        self.reset()

    def step(self, action):
        # TODO: change rID architecutre
        obs = self.observation_single(1)
        action2, _ = self.model_trained.predict(obs)

        agent1_grasping = self.env.objective_manager.has_pickup(0)
        agent2_grasping = self.env.objective_manager.has_pickup(1)
        carried = agent1_grasping and agent2_grasping

        if carried and action2 == action:
            self.env.move_robots(action, 0)
            self.env.move_robots(action2, 1)
            self.env.move_objectives(0)
            self.env.update_grid()
        elif not carried:
            if not agent1_grasping:
                self.env.move_robots(action, 0)
                self.env.update_grid()

            if not agent2_grasping:
                self.env.move_robots(action2, 1)
                self.env.update_grid()

        reward, done = self.env.reward_manager.observe(self.env, self.env.robots[0],
                                                       action)  # check if pickup and dropoff is successful

        done = self.current_step >= self.ep_length or done

        # determine data for input layer
        self.state = self._input_data(0)

        self.current_step += 1

        return self.state, reward, done, {}

    def reset(self):
        self.current_step = 0
        self.num_resets += 1
        self.steps_beyond_done = None
        self.done = False
        self.env.reset(self.num_resets)
        self.state = self._input_data(0)

        return self.state  # reward, done, info can't be included

    # scheme: agent pos, pickup pos, dropoff pos, carrying

    def _input_data(self, robotID):
        data = self.env.all_agents_position(), \
               self.env.objective_manager.pickup_get_positions_np(), \
               self.env.objective_manager.dropoff_get_positions_np(), \
               self.env.objective_manager.has_pickup(robotID)
        shape = np.concatenate(data, axis=None)
        return shape.reshape(1, self.N_DISCRETE_OBSERVATION)

    def observation_single(self, robotID):
        data = self.env.robot_position(robotID), \
               self.env.objective_manager.pickup_get_positions_np(), \
               self.env.objective_manager.dropoff_get_positions_np(), \
               self.env.objective_manager.has_pickup(robotID)
        shape = np.concatenate(data, axis=None)
        return shape.reshape(1, 7)

    def _observation_state(self):
        data = self.env.objective_manager.pickup_get_positions()

        return data

    def get_env(self):
        return self.env

    def render(self, mode='human'):
        pass

    def close(self):
        pass
