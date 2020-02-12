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

    # calculate the points after a move has been made
    def validate(self, env):
        reward = 0
        done = False

        for agent in env.robots:
            # single reward are rewards obtained by a single unit
            single_reward, carrying = self.check_carrier(agent)
            reward += single_reward

            if not carrying:
                return self.punish(), carrying, False  # not done yet

            single_reward, done = self.check_dropoff(agent)
            reward + single_reward + self.punish(), carrying, done  # done if pickup is on dropoff

        return reward, done

    def check_carrier(self, agent):
        result = 0, False
        # checks if the agent receives the carrier or not
        if agent.check_carrier():
            result = 0 if agent.rewarded else 10, True  # return reward of 10 if not rewarded before
            agent.rewarded = True
        return result

    def check_dropoff(self, agent):
        if agent.pickupObj.target_reached(self.dropoff):
            return 10, True

        return 0, False

    def punish(self, env_size=None):  # doesnt have the carrier, check if on dropoff zones
        return -1  # / (env_size[0] * env_size[1])

    # TODO
    def check_collision(self, env, agent_pos):
        collision = []
        # only check if agent has collision with
        for dummy in env.robots:
            if dummy.get_position() == agent_pos:
                collision.append(agent_pos)

        return collision
