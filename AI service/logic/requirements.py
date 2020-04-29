"""Object class for target/goal requirements
How the rewards are aggregated:
- Agents lose -1 for every move they do (except for when they have the pickup)
- Agents win 10 when picking up the objective
- Agents win 10 when dropping the objective
"""

import numpy as np


class Requirements(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid):
        self.grid = grid

    # calculate the points after a move has been made
    def validate(self, env, agent, actionID):
        # we are using separated reward function
        reward, carrying = self.check_carrier(agent, env.objective_manager)

        punishment = self.punish(agent, actionID)
        punishment += self.punish_collision(agent.get_position())

        if not carrying:
            return punishment + reward, False  # not done yet

        # check if the agent has reached the dropoff area
        single_r, done = self.check_dropoff(agent, env.objective_manager)
        reward += single_r

        return reward + punishment, done  # done if pickup is on dropoff

    def check_carrier(self, agent, obj_manager):
        result = 0, False
        # checks if the agent receives the carrier or not
        if agent.id in obj_manager.get_robot_objective_dict():
            result = 0 if agent.rewarded else 10, True  # return reward of 10 if not rewarded before
            agent.rewarded = True
        return result

    def check_dropoff(self, agent, obj_manager):
        if self.grid.check_pickup_delivery(agent.id, obj_manager):
            reward = obj_manager.get_delivery_reward(agent.id)
            return reward, True

        return 0, False

    def punish(self, agent, actionID):
        punishment = 0  # default punishment

        # if action is wait, punish twice as much
        if actionID == 0:
            punishment = -0.1

        return punishment  # / (env_size[0] * env_size[1])

    def punish_collision(self,  agent_pos):
        collision = self.grid.check_collision(agent_pos)

        if collision:
            return -10
        return 0
