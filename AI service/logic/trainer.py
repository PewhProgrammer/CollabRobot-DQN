"""Core ML module for predicting the next move of the robots
"""

from routes import render_env
import io_functions.game_logger as logger
from logic.DQN import DQN
from containers.env_wrapper import *


class Trainer(object):

    def __init__(self, gym_wrapper, params):
        self._gym_wrapper = gym_wrapper
        self.dqn_agents = [DQN(env=gym_wrapper, params=None)]

    def learn(self, timesteps=10000):
        # updateTargetNetwork = 1000

        ep_length = self._gym_wrapper.get_episode_len()
        overall_steps = 0
        episode = 0

        while overall_steps < timesteps:
            episode += 1
            self._gym_wrapper.reset()
            states = [self._gym_wrapper.input_data(i) for i in range(len(self.dqn_agents))]
            acc_rewards = {0: 0, 1: 0}
            # logger.save_init(self._gym_wrapper.get_env())
            for step in range(ep_length):
                overall_steps += 1
                # identifier = "E" + str(self._gym_wrapper.get_env().episode) + "_S" + str(step)
                for i, dqn_agent in enumerate(self.dqn_agents):  # Iterate over all agents
                    cur_state = states[i]
                    action = dqn_agent.act(cur_state)
                    new_state, reward, agent_done, _ = self._gym_wrapper.step(action)
                    acc_rewards[i] += reward

                    dqn_agent.remember(cur_state, action, reward, new_state, agent_done)

                    dqn_agent.replay()  # internally iterates default (prediction) model
                    # dqn_agent.target_train()  # iterates target model

                    states[i] = new_state

                # logger.save_state(self._gym_wrapper.get_env(), identifier)

                if self._gym_wrapper.get_env().objective_manager.is_done():  # check if every objective has been fufilled
                    break
            if episode % 100 == 0:
                print("Logged no. {} trial with {} epsilon".format(str(episode), self.dqn_agents[0].epsilon))
                print("Rewards: {}".format(acc_rewards))
                # logger.save_end(self._gym_wrapper.get_env(), acc_rewards)

        # return dqn_agent.out, dqn_agent.model

        print('Finished Training Session. Saving model and weights')
        episode = 'omega'
        self.dqn_agents[0].save_model("trial-{}.model".format(episode))

        print('Overall timesteps: {}'.format(overall_steps))

    def save(self):
        pass
        # self.dqn_agent.save_model("trial-{}.model".format(trial))

    def load(self):
        pass

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
