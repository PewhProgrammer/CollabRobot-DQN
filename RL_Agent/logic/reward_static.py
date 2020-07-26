"""Object class for target/goal requirements
This is a negative reinforcement.

How the rewards are aggregated:
- Agents lose default_punishment for every move they do (except for when they have the pickup)
- Agents lose collision_punishment for every collision it performs
- Agents win p_reward when picking up the objective
- Agents win d_reward when dropping the objective
"""

import numpy as np


# REWARD FUNCTION
class Reward_Static(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid, cfg):
        self.grid = grid
        self.p_reward = cfg["reward_conf"][1]
        self.d_reward = cfg["reward_conf"][3]
        self.collision_punishment = cfg["reward_conf"][4]
        self.default_punishment = cfg["reward_conf"][5]

    # calculate the points after a move has been made
    def observe(self, env, agent, actionID):
        # we are using separated reward function
        reward, carrying = self.reward_on_grasping(agent, env.objective_manager)

        punishment = self.punish(agent, actionID)

        if not carrying:
            return punishment + reward, False  # not done yet

        # check if the agent has reached the dropoff area
        single_r, done = self.reward_on_dropoff(agent, env.objective_manager)
        reward += single_r

        return reward + punishment, done  # done if pickup is on dropoff

    def reward_on_grasping(self, agent, obj_manager):
        result = 0, False
        # checks if the agent receives the carrier or not
        if agent.id in obj_manager.get_robot_objective_dict():
            result = 0 if agent.rewarded else self.p_reward, True  # return reward of 10 if not rewarded before
            agent.rewarded = True
        return result

    def reward_on_dropoff(self, agent, obj_manager):
        if self.grid.check_pickup_delivery(agent.id, obj_manager):
            reward = obj_manager.get_delivery_reward(agent.id)  # ignore reward output
            return self.p_reward + self.d_reward, True

        return 0, False

    def punish(self, agent, actionID):
        punishment = self.default_punishment  # default punishment

        # check collision
        agent_pos = agent.get_position()
        punishment += self.punish_collision(agent_pos)

        return punishment  # / (env_size[0] * env_size[1])

    def punish_collision(self,  agent_pos):
        collision = self.grid.check_collision(agent_pos)

        if collision:
            return self.collision_punishment
        return 0
