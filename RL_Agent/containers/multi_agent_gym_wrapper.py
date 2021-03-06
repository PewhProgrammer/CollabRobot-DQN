import gym
import numpy as np

from gym import spaces

from containers.environment import Environment


class MultiAgentCustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, config=None, model_trained=None, single=True, ep_length: int = 50):
        super(MultiAgentCustomEnv, self).__init__()

        self.config = config
        config["agents"] = 2

        self.single_trained = single
        self.model_trained = model_trained
        self.env = Environment(config=config)
        # raise AttributeError("One must supply either a maze_file path (str) or the maze_size (tuple of length 2)")

        self.env_size = (config["width"], config["height"])

        # Define action and observation space
        # They must be gym.spaces objects

        self.N_DISCRETE_ACTIONS = 5
        self.N_DISCRETE_OBSERVATION = config["observation_space"]
        self.N_DISCRETE_OBSERVATION_SINGLE = config["observation_space"]

        if config["agents"] == 2:
            # add the positions (2) and pickup data (1)
            self.N_DISCRETE_OBSERVATION += 3

        if config["sensor_information"]:
            self.N_DISCRETE_OBSERVATION += 8
            self.N_DISCRETE_OBSERVATION_SINGLE += 8

        if self.config["distance_information"]:
            self.N_DISCRETE_OBSERVATION += 2  # only for learning partner

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
        # TODO: change rID architecutre
        if self.single_trained:
            obs = self.observation_single(1)
        else:
            obs = self.input_data(1)
        action2, _ = self.model_trained.predict(obs)

        agent1_grasping = self.env.objective_manager.has_pickup(0)
        agent2_grasping = self.env.objective_manager.has_pickup(1)
        carried = agent1_grasping and agent2_grasping

        if self.config["distance_information"]:
            reward, done = self.update_allocation(action, action2, carried, agent1_grasping, agent2_grasping)
        else:
            reward, done = self.update_collaboration(action, action2, carried, agent1_grasping, agent2_grasping)

        info = {}
        if done:
            self.successes += 1
            info["is_success"] = 1
        elif self.current_step >= self.ep_length:
            info["is_success"] = 0

        done = self.current_step >= self.ep_length or done

        # determine data for input layer
        self.state = self.input_data(0)

        self.current_step += 1

        return self.state, reward, done, info

    def update_collaboration(self, action, action2, carried, agent1_grasping, agent2_grasping):
        nullify_reward = 1
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
        else:  # carried but action differs; deserves no points
            nullify_reward = 0

        reward, done = self.env.reward_manager.observe(self.env, self.env.robots[0],
                                                       action)  # check if pickup and dropoff is successful

        # nullify the reward if action differs during carrying in multiple setup
        reward *= nullify_reward

        return reward, done

    def update_allocation(self, action, action2, carried, agent1_grasping, agent2_grasping):
        negate_reward = -1

        self.env.move_robots(action, 0)
        self.env.move_robots(action2, 1)
        if agent1_grasping:
            self.env.move_objectives(0)
        if agent2_grasping:
            self.env.move_objectives(1)
        self.env.update_grid()
        reward, done = self.env.reward_manager.observe(self.env, self.env.robots[0],
                                                       action)

        reward2, done2 = self.env.reward_manager.observe(self.env, self.env.robots[1],
                                                         action2)

        done = done or done2

        # nullify the reward if the agent was too far away from the pickup
        if self.env.robots[0].dist_to_pickup > self.env.robots[1].dist_to_pickup:
            # punish agent1 when he is trying to move
            y, x = self.env.robots[0].get_latest_move_diff()
            if (x != 0 or y != 0) and reward > 0:
                reward *= negate_reward
            reward = min(0, reward)
        if self.env.robots[1].dist_to_pickup > self.env.robots[0].dist_to_pickup:
            # punish agent2 when he is trying to move
            y, x = self.env.robots[1].get_latest_move_diff()
            if (x != 0 or y != 0) and reward2 > 0:
                reward2 *= negate_reward
            reward2 = min(0, reward2)

        return reward + reward2, done

    def reset(self):
        self.current_step = 0
        self.num_resets += 1
        self.steps_beyond_done = None
        self.done = False
        self.env.reset(self.num_resets)
        self.state = self.input_data(0)

        return self.state  # reward, done, info can't be included

    # scheme: agent pos, pickup pos, dropoff pos, carrying
    def input_data(self, robotID):
        data = self.env.all_agents_position(first=robotID), \
               self.env.objective_manager.pickup_get_positions_np(), \
               self.env.objective_manager.dropoff_get_positions_np(), \
               self.get_all_pickups(first=robotID)

        if self.config["sensor_information"]:
            tmp = list(data) + self.env.grid.get_sensoric_distance(self.env.robot_position(robotID))
            data = tuple(tmp)

        if self.config["distance_information"]:
            # compute the distance to the pickup object
            tmp = list(data)
            tmp.append(self.env.robots[robotID].dist_to_pickup)
            # partners initial distance to pickup
            tmp.append(self.env.robots[0 if robotID == 1 else 1].dist_to_pickup)
            data = tuple(tmp)

        shape = np.concatenate(data, axis=None)
        return shape.reshape(1, self.N_DISCRETE_OBSERVATION)

    def observation_single(self, robotID):
        data = self.env.robot_position(robotID), \
               self.env.objective_manager.pickup_get_positions_np(), \
               self.env.objective_manager.dropoff_get_positions_np(), \
               self.env.objective_manager.has_pickup(robotID)

        if self.config["sensor_information"]:
            tmp = list(data) + self.env.grid.get_sensoric_distance(self.env.robot_position(robotID))
            data = tuple(tmp)

        shape = np.concatenate(data, axis=None)
        return shape.reshape(1, self.N_DISCRETE_OBSERVATION_SINGLE)

    def get_all_pickups(self, first=0):
        pickup_array = [self.env.objective_manager.has_pickup(first)]  # empty regular list
        for i in range(self.config["agents"]):
            if i != first:
                pickup_array.append(self.env.objective_manager.has_pickup(i))

        return np.array(pickup_array)

    def _observation_state(self):
        data = self.env.objective_manager.pickup_get_positions()

        return data

    def get_env(self):
        return self.env

    def render(self, mode='human'):
        pass

    def close(self):
        pass
