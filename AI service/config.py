# DEFAULT PARAMETERS FOR NETWORK

default = {'activation': 'relu',
           'optimizer': 'Adam',
           'losses': 'mse',
           'hidden_layers': [0],
           'dropout': [0],
           'batch_size': [0],
           'epochs': 500,  # uses early stopping
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
    "agents": 1,
    "pickup": {1: [(2, 1), (3, 1)]},
    "dropoff": {1: [(3, 3), (4, 3)]},
    "dummies": 0
}
