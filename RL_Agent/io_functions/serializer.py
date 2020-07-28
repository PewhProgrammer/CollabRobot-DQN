"""Helper class for functional methods
"""

import json


def export_dict_to_string(x):
    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


def export_state(env, state_id="NONE"):
    """
    :param state_id:
    :param env:
    :return: JSON object in string
    """

    x = {
        "id": str(state_id),
        "locations": {"pickup": list(env.objective_manager.pickup_get_positions_np()),
                      "agents": env.robot_positions()},
        "collisions": [],
        "action": env.last_action,  # TODO: change to several actions in multenv
    }

    return json.dumps(x, default=lambda o: o.__dict__, separators=(',', ':'))


def export_end_state(env, r, completed, min_steps, steps_p):
    """
    :param completed:
    :param env:
    :param r:
    :return: JSON object in string
    """

    x = {
        "acc_rewards": r,
        "completed": completed,
        "picked_up": env.reached_pickups(),
        "min_steps_required": min_steps,
        "steps_performed": steps_p
    }

    return x


def export_start_state(env):
    """
        :param env:
        :return: JSON object
        """
    x = {
        "episode": 'E' + str(env.episode),
        "width": env.width,
        "height": env.height,
        "start_locations": {"pickup": list(env.objective_manager.pickup_get_positions_np()),
                            "dropoff": list(env.objective_manager.dropoff_get_positions_np()),
                            "agents": env.robot_positions()}
    }

    return x
