"""Object class for target/goal requirements
"""


class Requirements(object):
    pickup = 0
    dropoff = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, pickup, dropoff):
        self.pickup = pickup
        self.dropoff = dropoff

    def validate(self, agent, map, env):
        reward, carrying = self.check_carrier(agent, map)  # done if pickup is reached
        if not carrying:
            return reward + self.punish(agent, map), carrying

        x, y = agent.get_position()
        env.pickup = map.encode(x, y)  # set pickup to agents position

        reward2, done = self.check_dropoff(agent, map)
        return reward + reward2, done  # done if pickup is on dropoff

    def check_carrier(self, agent, map):
        if agent.get_carrier():  # check if agent has carrier
            return 0, True

        agent_x, agent_y = agent.get_position()
        if self.pickup == map.encode(agent_x, agent_y):
            agent.set_carrier(True)
            return 3, True

        return 0, False

    def check_dropoff(self, agent, map):
        agent_x, agent_y = agent.get_position()
        if self.dropoff == map.encode(agent_x, agent_y):
            return 20, True

        return -1, False

    def punish(self, agent, map):  # doesnt have the carrier, check if on dropoff zone
        agent_x, agent_y = agent.get_position()
        if self.dropoff == map.encode(agent_x, agent_y):
            return -1

        return -1

