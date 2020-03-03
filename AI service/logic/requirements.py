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
    def validate(self, agent):

        # we are using separated reward function
        reward, carrying = self.check_carrier(agent)

        if not carrying:
            return self.punish(agent) + reward, False  # not done yet

        single_r, done = self.check_dropoff(agent)
        reward += single_r

        return reward + self.punish(agent), done  # done if pickup is on dropoff

    def check_carrier(self, agent):
        result = 0, False
        # checks if the agent receives the carrier or not
        if agent.has_pickup():
            result = 0 if agent.rewarded else 10, True  # return reward of 10 if not rewarded before
            agent.rewarded = True
        return result

    def check_dropoff(self, agent):
        x, y = agent.get_position()
        if self.grid.check_pickup_delivery(x, y):
            return 10, True

        return 0, False

    def punish(self, agent):
        punishment = -1

        if agent.has_pickup():
            punishment = -0.8

        return punishment  # / (env_size[0] * env_size[1])

    # TODO
    def check_collision(self, env, agent_pos):
        collision = []
        # only check if agent has collision with
        for dummy in env.robots:
            if dummy.get_position() == agent_pos:
                collision.append(agent_pos)

        return collision
