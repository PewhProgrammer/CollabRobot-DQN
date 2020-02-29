"""Core ML module for predicting the next move of the robots
"""

from routes import render_env
import io_functions.game_logger as logger
from logic.DQN import DQN
from containers.env_wrapper import *


def game_loop(envW, sio=None, params=None):
    trials = params['epochs']
    trial_len = 200

    # updateTargetNetwork = 1000
    # dqn_agent = DQN(env=envW, params=params)
    step = 0

    dqn_agents = [DQN(env=envW, params=params), DQN(env=envW, params=params)]

    for trial in range(trials):
        envW.reset(trial)
        states = [envW.input_data(i) for i in range(len(dqn_agents))]
        acc_rewards = 0
        logger.save_init(envW.get_env())
        done = False
        for step in range(trial_len):
            identifier = "E" + str(envW.get_env().episode) + "_S" + str(step)

            for i, dqn_agent in enumerate(dqn_agents):  # Iterate over all agents
                cur_state = states[i]
                action = dqn_agent.act(cur_state)
                new_state, reward, single_done, _ = envW.step(action, i)
                done = done and single_done  # check if every agent is done with its task
                acc_rewards += reward

                dqn_agent.remember(cur_state, action, reward, new_state, single_done)

                dqn_agent.replay()  # internally iterates default (prediction) model
                dqn_agent.target_train()  # iterates target model

                states[i] = new_state

            # render_env(sio)
            logger.save_state(envW.get_env(), identifier)

            if done:
                break
        if step >= 50:
            print("Failed to complete in trial {}".format(trial))
            # print(params['losses'], dqn_agent.out.history['loss'][-1])
            # if step % 10 == 0:
            # dqn_agent.save_model("trial-{}.model".format(trial))
        else:
            print("Completed in trial {} with {} steps".format(trial, step))
            # print(params['losses'], dqn_agent.out.history['loss'][-1])
            # dqn_agent.save_model("success.model")
            # break

        logger.save_end(envW.get_env(), acc_rewards)

    # return dqn_agent.out, dqn_agent.model

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
