"""Core ML module for predicting the next move of the robots
"""

import random
# import tensorflow as tf
from common.env_wrapper import EnvWrapper
from routes import render_env
import numpy as np
import time
from data.DQN import DQN
from common.environment import get_env

envWrap = None


def init_predictor(config):
    global envWrap
    envWrap = EnvWrapper(config)


def run_prediction(sio):
    env = envWrap

    trials = 1000
    trial_len = 500

    # updateTargetNetwork = 1000
    dqn_agent = DQN(env=env)
    steps = []
    start_time = time.time()
    move = 0
    timeline = 5
    for trial in range(trials):
        cur_state = env.reset().reshape(1, 3)
        for step in range(trial_len):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)

            # reward = reward if not done else -20
            new_state = new_state.reshape(1, 3)
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            dqn_agent.replay()  # internally iterates default (prediction) model
            dqn_agent.target_train()  # iterates target model

            render_env(env.render_state())
            sio.sleep(0.000001)
            elapsed_time = time.time() - start_time
            if elapsed_time > timeline:
                timeline += 5
                # print("{} actions per 5 seconds".format(move))
                move = 0

            move += 1

            cur_state = new_state
            if done:
                break
        if step >= 199:
            print("Failed to complete in trial {}".format(trial))
            # if step % 10 == 0:
                # dqn_agent.save_model("trial-{}.model".format(trial))
        else:
            print("Completed in {} trial with {} steps".format(trial, step))
            # dqn_agent.save_model("success.model")
            # break

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
