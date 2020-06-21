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
    "dummies": 4,
    "observation_space": 7,
    "reward": "gradient",
    "sensor_information": True
}

small_room_single_test = {
    "id": 3,
    "width": 10,
    "height": 6,
    "map": ["maps/small_room/", 150],
    "agents": 1,
    "dummies": 0,
    "observation_space": 7,
    "reward": "static",
    "load_model": "single_gradient_dynamic_negative"
}

wide_room_single = {
    "id": 3,
    "width": 16,
    "height": 16,
    "map": ["maps/wide_room/empty.map", 1],
    "agents": 1,
    "dummies": 4,
    "observation_space": 7,
    "reward": "gradient",
    "sensor_information": True
}

narrow_passages_single = {
    "id": 4,
    "width": 16,
    "height": 16,
    "map": ["maps/narrow_passages/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "observation_space": 7,
    "reward": "gradient"
}

small_narrow_passages_single = {
    "id": 5,
    "width": 13,
    "height": 7,
    "map": ["maps/small_narrow_passages/empty.map", 1],
    "agents": 1,
    "dummies": 0,
    "observation_space": 7,
    "reward": "gradient",
    "sensor_information": True
}

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
