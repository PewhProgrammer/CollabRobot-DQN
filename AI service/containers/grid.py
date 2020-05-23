"""Object class for Grid manipulation and shortest path algorithm
"""

from common.robot import Robot


class Grid(object):

    # The class "constructor" - It's actually an initializer
    def __init__(self, grid, config=None):
        self._stored_positions = []
        self._width = config["width"]
        self._height = config["height"]
        self.grid = grid

    def update(self, robots: [Robot], obj_manager):
        self.reset_grid()
        for idx, i in robots.items():
            y, x = i.get_position()
            self._stored_positions.append((y, x))
            try:
                self.grid[y][x].append(idx)
            except IndexError:
                print("{}, {}".format(x, y))

        for key, objective in obj_manager.get_objectives().items():
            # objective -> Objectives
            p_pos = objective.get_pickup_np()
            d_pos = objective.get_dropoff_np()
            y, x = p_pos[0], p_pos[1]
            y1, x1 = d_pos[0], d_pos[1]

            self._stored_positions.append((y, x))
            self.grid[y][x].append("P" + str(key))

            self._stored_positions.append((y1, x1))
            self.grid[y1][x1].append("D" + str(key))

    def check_pickup_delivery(self, agentID, obj_manager):
        """
        looks if agentPos in grid has pickup and dropoff object
        :return: Boolean value indicating if agent successfully dropped of the pickup target
        """
        get_obj = obj_manager.get_robot_objective_dict()
        if agentID not in get_obj:
            return False

        objective_id = get_obj[agentID]
        objective = obj_manager.get_objectives()[objective_id]
        return objective.is_delivered()

    def check_collision(self, pos):
        # if agent collided with obstacles and if pickup collided with anything else
        agent_num = 0
        for i in self.grid[pos[0]][pos[1]]:

            if is_number(i):
                agent_num += 1

            if i == '#' or agent_num > 1 or (not is_number(i) and i.startswith('P')):  # or i.startswith('X')
                return True

        return False

    def check_collision_as_pickup(self, pos):
        # if agent collided with obstacles and if pickup collided with anything else
        agent_num = 0
        for i in self.grid[pos[0]][pos[1]]:

            if is_number(i):
                agent_num += 1

            if i == '#' or agent_num > 1:  # or i.startswith('X')
                return True

        return False

    def reset_grid(self):
        for y, x in self._stored_positions:
            if '#' in self.grid[y][x]:
                self.grid[y][x] = ['#']
            else:
                self.grid[y][x] = []
        self._stored_positions = []

    def check_occupancy_free(self, x, y):
        return len(self.grid[y][x]) == 0


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
