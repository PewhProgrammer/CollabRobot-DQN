"""Object class for target/goal requirements
"""

import numpy as np


class Requirements(object):
    pickup = 0
    dropoff = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, pickup, dropoff):
        self.pickup = pickup
        self.dropoff = dropoff

    def validate(self, env):

        agent = env.robot
        agentPos = np.asarray(agent.get_position())
        reward, carrying = self.check_carrier(agent, agentPos)  # done if pickup is reached
        if not carrying:
            return self.punish(env.size), carrying, False  # not done yet

        env.pickup = agentPos  # set pickup to agents position

        if reward == 1:  # just picked up the pickup
            return reward, carrying, False

        reward, done = self.check_dropoff(agentPos)
        return reward + self.punish(env.size), carrying, done  # done if pickup is on dropoff

    def check_carrier(self, agent, agentPos):
        if agent.get_carrier():  # check if agent has carrier
            return 0, True

        if np.array_equal(self.pickup, agentPos):
            agent.set_carrier(True)
            return 1, True

        return 0, False

    def check_dropoff(self, agentPos):
        if np.array_equal(self.dropoff, agentPos):
            return 1, True

        return 0, False

    def punish(self, env_size):  # doesnt have the carrier, check if on dropoff zones
        return -0.1 / (env_size[0] * env_size[1])
