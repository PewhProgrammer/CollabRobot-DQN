"""Helper class for functional methods
"""

import json
import common.map


def update_env_encode(board):
    """
    :param board:
    :return: JSON object
    """
    pX, pY = board.map.decode(board.pickup)
    dX, dY = board.map.decode(board.dropoff)
    x = {
        "agents": board.units,
        "pickupX": pX,
        "pickupY": pY
    }

    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


def new_env_encode(board):
    """
        :param board:
        :return: JSON object
        """
    pX, pY = board.map.decode(board.pickup)
    dX, dY = board.map.decode(board.dropoff)
    x = {
        "width": board.width,
        "height": board.height,
        "pickupX": pX,
        "pickupY": pY,
        "dropoffX": dX,
        "dropoffY": dY,
        "agents": board.units
    }

    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


