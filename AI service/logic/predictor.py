"""Core ML module for predicting the next move of the robots
"""

# import os
# import tensorflow as tf
import common.environment as env
from routes import render_state


def init_predictor(width, height, size):
    env.make_env(width, height, size)


def run_prediction(sio):
    epochs = 0
    penalties, reward = 0, 0

    done = False
    while not done:
        action = env.action_space_sample()
        state, reward, done = env.step(action)

        sio.sleep(0.02)
        render_state(state)

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
