"""Object class for target/goal requirements
This is a gradient reinforcement based on distance.

How the rewards are aggregated:
- Agents lose default_punishment for every move they do (except for when they have the pickup)
- Agents lose collision_punishment for every collision it performs
- Agents win p_reward when picking up the objective
- Agents win d_reward when dropping the objective
"""

import numpy as np
import math

from common.robot import Movement
from logic.reward_gradient import compute_euc_dist


## CHANGE LOG
# If stuck or perform unecessary grasp, do not reward anything
# removed negative punishment


# REWARD FUNCTION
class RewardGradientCustom(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid, cfg):
        self.grid = grid
        self.p_reward = cfg["reward_conf"][0]
        self.p_reward_final = cfg["reward_conf"][1]
        self.d_reward = cfg["reward_conf"][2]
        self.d_reward_final = cfg["reward_conf"][3]
        self.collision_punishment = cfg["reward_conf"][4]
        self.default_punishment = cfg["reward_conf"][5]

    # calculate the points after a move has been made
    def observe(self, env, agent, actionID):
        # we are using separated reward function
        reward, carrying = self.reward_on_grasping(agent, env, actionID)

        punishment = self.punish(agent, actionID)

        if not carrying:
            return punishment + reward, False  # not done yet

        # check if the agent has reached the dropoff area
        single_r, done = self.reward_on_dropoff(agent, env, actionID)
        reward += single_r

        return reward + punishment, done  # done if pickup is on dropoff

    def reward_on_distance(self, agent, obj_manager, max_dist, pickup=True):
        # can only award maximum of p_reward

        objective = obj_manager.get_objectives()[0]
        if pickup:
            x1, y1 = agent.get_position()
            x2, y2 = objective.get_pickup_pos()
            obj_reward_fraction = self.p_reward
        else:
            x1, y1 = objective.get_pickup_pos()
            x2, y2 = objective.get_dropoff_pos()
            obj_reward_fraction = self.d_reward

        # compute euclidean distance
        euc_dist = math.pow(compute_euc_dist(x1, y1, x2, y2), 0.4)
        return obj_reward_fraction - (obj_reward_fraction * (euc_dist / math.pow(max_dist, 0.4)))

    def reward_on_grasping(self, agent, env, action_id):
        obj_manager = env.objective_manager

        # checks if the agent receives the carrier or not
        if agent.id in obj_manager.get_robot_objective_dict():
            result = 0 if agent.rewarded else self.p_reward_final, True
            agent.rewarded = True
            return result

        if action_id == Movement.GRASP.value:  # or agent.is_stuck(action_id):
            return 0, False

        return self.reward_on_distance(agent, obj_manager, env.max_euc_dist), False

    def reward_on_dropoff(self, agent, env, action_id):
        obj_manager = env.objective_manager
        if self.grid.check_pickup_delivery(agent.id, obj_manager):
            return self.d_reward_final, True

        if action_id == Movement.GRASP.value:  # or agent.is_stuck(action_id):
            return 0, False

        return self.reward_on_distance(agent, obj_manager, env.max_euc_dist, pickup=False), False

    def punish(self, agent, action_id):
        punishment = self.default_punishment  # default punishment

        # punish for being stuck
        if agent.is_stuck(action_id):
            punishment += self.collision_punishment

        # check collision
        agent_pos = agent.get_position()
        punishment += self.punish_collision(agent_pos)

        return punishment  # / (env_size[0] * env_size[1])

    def punish_collision(self, agent_pos):
        collision = self.grid.check_collision(agent_pos)

        if collision:
            return self.collision_punishment
        return 0


if __name__ == "__main__":
    d_reward = 15
    obj_reward_frac = d_reward / 10
    max_dist = compute_euc_dist(0, 0, 13, 10)
    dist = compute_euc_dist(2, 5, 3, 5)

    res = obj_reward_frac - (obj_reward_frac * (dist / max_dist))
    print("reward: {}".format(res))
