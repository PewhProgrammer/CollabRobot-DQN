# DEFAULT PARAMETERS FOR NETWORK

default = {'activation': 'relu',
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

map_5x5 = {
    "id": 1,
    "width": 5,
    "height": 5,
    "agents": 2,
    "pickup": {1: [(2, 1), (3, 1)]},
    "dropoff": {1: [(3, 3), (4, 3)]},
    "dummies": 0,  # they are not moving rn, left unimplemented
    "observation_space": 13
}

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
    "map": "maps/small_room.map",
    "agents": 1,
    "dummies": 0,
    "observation_space": 7
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


