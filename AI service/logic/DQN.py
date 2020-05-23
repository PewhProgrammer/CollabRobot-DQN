import numpy as np
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from collections import deque

tf.get_logger().setLevel('INFO')

config = tf.compat.v1.ConfigProto( device_count = {'GPU': 1 , 'CPU': 1} )
sess = tf.compat.v1.Session(config=tf.ConfigProto(log_device_placement=True))
keras.backend.set_session(sess)


class DQN(object):

    def __init__(self, env, params=None):
        self.env = env
        self.memory = deque(maxlen=2000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995  # default was 0.995
        self.learning_rate = 0.001
        self.tau = .05

        # "hack" implemented by DeepMind to improve convergence
        if params is None:
            self.model = self.create_model()
        else:
            self.model = self.create_parametrised_model(params)
        self.target_model = self.create_model()
        self.out = None  # model.fit output

    def create_model(self):

        model = Sequential()
        model.add(Dense(24, input_dim=self.env.observation_space,
                        activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def create_parametrised_model(self, params):
        model = Sequential()
        model.add(Dense(24, input_dim=self.env.observation_space,
                        activation=params['activation']))
        model.add(Dense(48, activation=params['activation']))
        model.add(Dense(24, activation=params['activation']))
        model.add(Dense(self.env.action_space.n))
        model.compile(optimizer=params['optimizer'], loss=params['losses'])

        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.out = self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)
