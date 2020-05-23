"""Object class for managing objectves. A objective can be classified as pickup or dropoff target
"""

import numpy as np
from common.objectives import Objectives

""" FOR TESTING PURPOSES ONLY IMPORTS """
import config
from containers.grid import Grid
from common.robot_factory import make_agent
from io_functions.map_reader import load_map


class Objective_Manager(object):

    def __init__(self, obj_dict):
        self._objectives_dict = obj_dict
        self._robot_objectives_dict = {}

    def perform_action(self, robot, grid):
        # is used in robots method move()

        # check if robot has objectives
        if robot.id not in self._robot_objectives_dict.keys():
            return False

        # Get objective obj
        objective_id = self._robot_objectives_dict[robot.id]
        objective = self._objectives_dict[objective_id]

        # compute new P pos
        newPos = objective.compute_new_pickup_pos(robot.get_latest_move_diff())

        # check if enough agents are carrying P
        not_enough_carriers = not self.get_carried()

        if newPos != objective.get_pickup_pos() and not_enough_carriers:
            self._robot_objectives_dict.pop(robot.id)  # degrasping
            return False

        # check if P is colliding with any immediate object when moved
        collided = grid.check_collision_as_pickup(newPos)
        if collided:
            self._robot_objectives_dict.pop(robot.id)  # collision happened, degrasping
            return False

        objective.set_position(newPos)
        return True

    def check_grasping_objective(self, robot):
        rY, rX = robot.get_position()
        pY, pX = self._objectives_dict[0].get_pickup_pos()

        det = abs(rY - pY) + abs(rX - pX)
        if det == 1:
            # check from which position
            self._robot_objectives_dict[robot.get_id()] = 0

    """ GETTER AND SETTER METHODS """

    def dropoff_get_positions_np(self) -> np.array:
        result_list = np.array([])
        for objective in self._objectives_dict.values():
            dropoff = objective.get_dropoff_np()
            result_list = np.concatenate((result_list, dropoff))

        return result_list

    def pickup_get_positions_np(self) -> np.array:
        result_list = np.array([])
        for objective in self._objectives_dict.values():
            pickup = objective.get_pickup_np()
            result_list = np.concatenate((result_list, pickup))

        return result_list

    def pickup_get_positions(self):
        result = ()
        for objective in self._objectives_dict.values():
            pickup = objective.get_pickup_pos()
            result = pickup

        return result

    def get_carried(self):
        carrying = len(self._robot_objectives_dict)
        objective = self._objectives_dict[0]
        return carrying >= objective.get_weight()

    def carriable(self, rID):
        if rID not in self._robot_objectives_dict:
            return False

        objective_id = self._robot_objectives_dict[rID]
        objective = self._objectives_dict[objective_id]

        carrying = 0
        for rID, oID in self._robot_objectives_dict.items():
            if oID == objective_id:
                carrying += 1

        if carrying >= objective.get_weight():
            return True
        return False

    def get_objectives(self):
        return self._objectives_dict

    def get_robot_objective_dict(self):
        return self._robot_objectives_dict

    def get_delivery_reward(self, agentID):
        get_obj = self.get_robot_objective_dict()
        if agentID not in get_obj:  # check if objective is available
            return 0

        objective_id = self.get_robot_objective_dict()[agentID]
        objective = self.get_objectives()[objective_id]
        return objective.delivery_reward()

    def has_pickup(self, agentID):
        return agentID in self._robot_objectives_dict.keys()

    def is_done(self):
        done = True
        for obj in self._objectives_dict.values():
            done = done and obj.is_delivered()

        return done


if __name__ == "__main__":
    conf = config.test_obj_manager_room

    width, height = conf["width"], conf["height"]
    loaded_map, objective_list = load_map(conf["map"], width, height)
    grid = Grid(loaded_map, conf)
    agent = make_agent(0, grid, width=width, height=height)
    obj_manager = Objective_Manager(objective_list)

    agent.move(5)  # grasp the object
    obj_manager.check_grasping_objective(agent)
    grid.update({0: agent}, obj_manager)
    agent.move(3)  # move to the right
    grid.update({0: agent}, obj_manager)
    obj_manager.perform_action(agent, grid)

    obj_manager.dropoff_get_positions_np()
    obj_manager.pickup_get_positions_np()

    print("Pickup delivered: {}".format(grid.check_pickup_delivery(0, obj_manager)))
    print("Rewarded: {}".format(obj_manager.get_delivery_reward(0)))
    print("Rewarded After: {}".format(obj_manager.get_delivery_reward(0)))

    exit(0)
