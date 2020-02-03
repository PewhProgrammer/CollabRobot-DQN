# DEFAULT PARAMETERS FOR NETWORK

default = {'activation': 'relu',
           'optimizer': 'Adam',
           'losses': 'mse',
           'hidden_layers': [0],
           'dropout': [0],
           'batch_size': [0],
           'epochs': 50,  # uses early stopping
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


map_10x10 = {
    "id": 1,
    "width": 10,
    "height": 10,
    "agents": 1,
    "agentPosX": 5,
    "agentPosY": 5,
    "pickupX": 2,
    "pickupY": 5,
    "dropoffX": 8,
    "dropoffY": 5
}

map_5x5 = {
    "id": 2,
    "width": 5,
    "height": 5,
    "agents": 1,
    "pickupX": 2,
    "pickupY": 1,
    "dropoffX": 4,
    "dropoffY": 2,
    "dummies": 1
}
