"""Helper class for functional methods
"""

import json
import common.map


def update_env_encode(board):
    """
    :param board:
    :return: JSON object
    """

    x = {
        "agents": {0:board.robot},
        "pickupX": board.pickup[0].item(),
        "pickupY": board.pickup[1].item()
    }

    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


def new_env_encode(board):
    """
        :param board:
        :return: JSON object
        """
    x = {
        "width": board.width,
        "height": board.height,
        "pickupX": board.pickup[0].item(),
        "pickupY": board.pickup[1].item(),
        "dropoffX": board.dropoff[0].item(),
        "dropoffY": board.dropoff[1].item(),
        "agents": {0:board.robot}
    }

    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


