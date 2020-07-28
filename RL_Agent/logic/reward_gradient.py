"""Object class for target/goal requirements
This is a gradient reinforcement based on distance.

How the rewards are aggregated:
- Agents lose default_punishment for every move they do (except for when they have the pickup)
- Agents lose collision_punishment for every collision it performs
- Agents win p_reward when picking up the objective
- Agents win d_reward when dropping the objective
"""

import numpy as np
from common.robot import Movement
import math


# REWARD FUNCTION
class RewardGradient(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid, cfg):
        self.mode = cfg["id"]
        self.grid = grid
        self.p_reward = cfg["reward_conf"][0]
        self.p_reward_final = cfg["reward_conf"][1]
        self.d_reward = cfg["reward_conf"][2]
        self.d_reward_final = cfg["reward_conf"][3]
        self.collision_punishment = cfg["reward_conf"][4]
        self.default_punishment = cfg["reward_conf"][5]

    # calculate the points after a move has been made
    def observe(self, env, agent, actionID):

        if self.mode == 6:
            # this is obstacle lane use case
            return self.update_obstacle_lane(env, agent, actionID)
        return self.update_basic(env, agent, actionID)

    def update_obstacle_lane(self,env, agent, actionID):
        punishment = self.punish(agent, actionID)

        # check if the agent has reached the dropoff area
        reward, done = self.reward_on_dropoff(agent, env, actionID)

        return reward + punishment, done  # done if pickup is on dropoff

    def update_basic(self, env, agent, actionID):
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

        if self.mode == 6:
            if self.grid.check_agent_on_dropoff(agent):
                return self.d_reward_final, True
        else:
            if self.grid.check_pickup_delivery(agent.id, obj_manager):
                return self.d_reward_final, True

        if action_id == Movement.GRASP.value:  # or agent.is_stuck(action_id):
            return 0, False

        return self.reward_on_distance(agent, obj_manager, env.max_euc_dist, pickup=False), False

    def punish(self, agent, action_id):
        punishment = self.default_punishment  # default punishment

        # punish for being stuck
        # if agent.is_stuck(action_id):
        #     punishment += self.collision_punishment

        # check collision
        punishment += self.punish_collision(agent)

        return punishment  # / (env_size[0] * env_size[1])

    def punish_collision(self, agent):
        agent_pos = agent.get_position()
        collision = self.grid.check_collision(agent_pos)

        if collision:
            agent.set_collided(True)
            return self.collision_punishment
        return 0


def compute_euc_dist(startX, startY, targetX, targetY):
    # compute euclidean distance
    return math.sqrt(pow(startX - targetX, 2) + pow(startY - targetY, 2))


if __name__ == "__main__":
    obj_reward_frac = 10
    max_dist = math.pow(compute_euc_dist(0, 0, 13, 8), 0.4)
    for i in range(10):
        i += 2
        dist = math.pow(compute_euc_dist(1, 1, i, i), 0.4)
        res = obj_reward_frac - (obj_reward_frac * (dist / max_dist))
        print("reward: {0} dist: {1}".format(res, i))
