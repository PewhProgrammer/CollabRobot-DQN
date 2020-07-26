# DEFAULT PARAMETERS FOR NETWORK

default_params = {'activation': 'relu',
                  'optimizer': 'Adam',
                  'losses': 'mse',
                  'hidden_layers': [0],
                  'dropout': [0],
                  'batch_size': [0],
                  'epochs': 4000,  # uses early stopping
                  'shape': ['triangle', 'brick'],
                  'early_stopping': [True],
                  'patience': [5],
                  }

talos_params = {'activation': ['relu', 'elu'],
                'optimizer': ['Nadam', 'Adam'],
                'losses': ['mse', 'mae', 'logcosh'],
                'hidden_layers': [1, 2, 3],
                'dropout': [0, 0.2, 0.5],
                'batch_size': [20, 30, 40],
                'epochs': [5],  # uses early stopping
                'shape': ['triangle', 'brick'],
                'early_stopping': [True],
                'patience': [5],
                }

# MAP

sample_easy = {
    "id": 2,
    "width": 31,
    "height": 11,
    "map": "maps/sample_easy.map",
    "agents": 1,
    "dummies": 0,
    "connected_objectives": [(1, 2)],
    "observation_space": 7
}

small_room_single = {
    "id": 3,
    "width": 10,
    "height": 6,
    "map": ["maps/small_room/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "p_weight": 1,
    "observation_space": 7,
    "reward": "gradient",
    # "reward_conf": [0.05, 500, 1, 500, -15, 0],
    "reward_conf": [1, 10, 10, 2000, 0, 0],
    "sensor_information": True,
    "timesteps": 3000000,
    "ep_length": 50,
    "prioritized": True,
    "dueling": True,
    "double-dqn": True,
    "exploration_frac": 0.1,
    "study_results": "./study/algorithm_test/concept-4/small_room/",
    "experiment_name": "experiment"
}

small_room_single_test = {**small_room_single, 'map': ["maps/small_room/", 150]}

normal_room_single = {
    "id": 4,
    "width": 13,
    "height": 8,
    "map": ["maps/normal_room/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "p_weight": 2,
    "observation_space": 7,
    "reward": "static",
    # "reward_conf": [0.05, 500, 1, 500, -15, 0],
    "reward_conf": [0, 5, 0, 15, -15, 0],
    "sensor_information": False,
    "timesteps": 500000,
    "ep_length": 50,
    "prioritized": True,
    "dueling": True,
    "double-dqn": True,
    "exploration_frac": 0.1,
    "study_results": "./study/algorithm_test/concept-3/normal_room/",
    "experiment_name": "experiment_double-dueling-prioritized"
}

normal_room_single_test = {**normal_room_single, 'map': ["maps/normal_room/", 150]}

wide_room_single = {
    "id": 3,
    "width": 16,
    "height": 16,
    "map": ["maps/wide_room/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "p_weight": 1,
    "observation_space": 7,
    "reward": "gradient",
    # "reward_conf": [0.05, 500, 1, 500, -15, 0],
    "reward_conf": [1, 10, 10, 2000, 0, 0],
    "sensor_information": False,
    "timesteps": 250000,
    "ep_length": 50,
    "prioritized": True,
    "dueling": True,
    "double-dqn": True,
    "exploration_frac": 0.1,
    "study_results": "./study/algorithm_test/sensor/wide_room/",
    "experiment_name": "experiment"
}

wide_room_single_test = {**wide_room_single, 'map': ["maps/wide_room/", 150]}

narrow_passages_single = {
    "id": 4,
    "width": 16,
    "height": 16,
    "map": ["maps/narrow_passages/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "p_weight": 1,
    "observation_space": 7,
    "reward": "custom",
    # "reward_conf": [0.05, 500, 1, 500, -15, 0],
    "reward_conf": [1, 10, 10, 2000, 0, 0],
    "sensor_information": False,
    "timesteps": 500000,
    "ep_length": 50,
    "prioritized": True,
    "dueling": True,
    "double-dqn": True,
    "exploration_frac": 0.1,
    "study_results": "./study/algorithm_test/concept-1/small_narrow/",
    "experiment_name": "experiment"
}

narrow_passages_single_test = {**narrow_passages_single, 'map': ["maps/narrow_passages/", 150]}

small_warehouse_single = {
    "id": 5,
    "width": 13,
    "height": 8,
    "map": ["maps/small_warehouse/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "p_weight": 1,
    "observation_space": 7,
    "reward": "gradient",
    # "reward_conf": [0.05, 500, 1, 500, -15, 0],
    "reward_conf": [1, 10, 10, 2000, 0, 0],
    "sensor_information": True,
    "timesteps": 500000,
    "ep_length": 50,
    "prioritized": True,
    "dueling": True,
    "double-dqn": True,
    "exploration_frac": 0.1,
    "study_results": "./study/algorithm_test/concept-2/small_warehouse/",
    "experiment_name": "experiment"
}

small_warehouse_single_test = {**small_warehouse_single, 'map': ["maps/small_warehouse/", 150]}

small_room_p2_multiple = {
    "id": 3,
    "width": 10,
    "height": 6,
    "map": "maps/small_room_p2.map",
    "agents": 2,
    "dummies": 0,
    "observation_space": 9
}

test_obj_manager_room = {
    "id": 3,
    "width": 4,
    "height": 4,
    "map": "../maps/test_obj_manager_room.map",
    "agents": 1,
    "dummies": 0,
    "observation_space": 7
}

if __name__ == '__main__':
    print(small_room_single_test)
