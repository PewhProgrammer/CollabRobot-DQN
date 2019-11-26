"""Core ML module for predicting the next move of the robots
"""

import random
# import tensorflow as tf
import common.environment as env
from routes import render_env
import numpy as np

q_table = None

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1


def init_predictor(config):
    width, height, size = config["width"], config["height"], config["agents"]
    if config["id"] == 1:
        width, height, size = config["width"], config["height"], config["agents"]
        env.make_env(width, height, size, config)
    else:
        env.make_env(width, height, size)
    global q_table
    q_table = np.zeros([width * height, 9])


def run_prediction(sio):
    total_epochs, total_penalties = 0, 0
    episodes = 100
    epochs = 0

    for x in range(episodes):
        env.env_reset()
        state = env.calc_state()
        epochs, penalties, reward, = 0, 0, 0
        done = False
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = env.action_space_sample()  # Explore action space
            else:
                movementID = np.argmax(q_table[state])
                action = env.get_movement(movementID, 0)  # Exploit learned values

            next_state, reward, done, board = env.step(action)
            # print(action[0])
            actionID = action[0].value

            old_value = q_table[state, actionID]
            next_max = np.max(q_table[next_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, actionID] = new_value

            if reward < -10:
                penalties += 1

            state = next_state
            epochs += 1

            if x == 99:
                sio.sleep(0.2)
                render_env(board)

        total_penalties += penalties
        total_epochs += epochs

    print(f"Results after {episodes} episodes:")
    print(f"Average timesteps per episode: {total_epochs / episodes}")
    print(f"Average penalties per episode: {total_penalties / episodes}")

    print(f"Current timesteps in test episode: {epochs}")

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
