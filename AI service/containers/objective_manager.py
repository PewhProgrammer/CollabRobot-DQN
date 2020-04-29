"""Object class for managing objectves. A objective can be classified as pickup or dropoff target
"""

import numpy as np
from common.objectives import Objectives


class Objective_Manager(object):

    def __init__(self, obj_dict, connected_objectives=""):
        # connected_objectives -> e.g. [(1,2)] means 1 and 2 are connected
        self._positions = []
        self._objectives_dict = obj_dict
        self._robot_objectives_dict = {}

    def move_position(self, robot):
        # is used in robots method move()

        # check if robot has objectives
        if robot.id not in self._robot_objectives_dict.keys():
            return False

        # check if pickup pieces are in reach
        objective_id = self._robot_objectives_dict[robot.id]
        objective = self._objectives_dict[objective_id]
        objective.pickup_move(robot.get_position())

        # for occupied in self._positions:
        #     # TODO: atm only works with 2 pickups
        #     if occupied[0] == movePos[0] and occupied[1] == movePos[1]:
        #         return False  # pickup would be moved onto another pickup spot
        #
        #     if abs(occupied[0] - movePos[0]) > 1 or abs(occupied[1] - movePos[1]) > 1:
        #         return False  # x,y-coordinate is too far apart
        #
        # # check if all pickup objects are occupied
        # if self.occupant < len(self._positions) and self._positions[idx] != movePos:
        #     # we want to move but not enough occupants
        #     return False
        #
        # self._positions[idx] = movePos
        # return True

    def assign_robot_to_objective(self, robotID, objectiveID):
        for value in self._robot_objectives_dict.values():
            if value == objectiveID:
                return
        self._robot_objectives_dict[robotID] = objectiveID

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

    def get_objectives(self):
        return self._objectives_dict

    def get_robot_objective_dict(self):
        return self._robot_objectives_dict

    def get_delivery_reward(self, agentID):
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
    obj_dict = {}
    obj_dict[1] = Objectives((1, 16), (2, 5))
    obj_dict[2] = Objectives((2, 15), (6, 23))
    obj_dict[3] = Objectives((3, 12), (7, 58))

    obj_manager = Objective_Manager(obj_dict)
    obj_manager.dropoff_get_positions_np()
    obj_manager.pickup_get_positions_np()
