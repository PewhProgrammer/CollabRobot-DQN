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

    dqn_agents = [DQN(env=envW, params=params)]

    for trial in range(trials):
        envW.reset(trial)
        states = [envW.input_data(i) for i in range(len(dqn_agents))]
        acc_rewards = {0: 0, 1: 0}
        logger.save_init(envW.get_env())
        for step in range(trial_len):
            identifier = "E" + str(envW.get_env().episode) + "_S" + str(step)
            for i, dqn_agent in enumerate(dqn_agents):  # Iterate over all agents
                cur_state = states[i]
                action = dqn_agent.act(cur_state)
                new_state, reward, agent_done, _ = envW.step(action, i)
                acc_rewards[i] += reward

                dqn_agent.remember(cur_state, action, reward, new_state, agent_done)

                dqn_agent.replay()  # internally iterates default (prediction) model
                dqn_agent.target_train()  # iterates target model

                states[i] = new_state

            # render_env(sio)
            logger.save_state(envW.get_env(), identifier)

            if envW.get_env().objective_manager.is_done():  # check if every objective has been fufilled
                break
        # if step >= 50:
            # print("Failed to complete in trial {} with {} steps".format(trial, step))
            # print(params['losses'], dqn_agent.out.history['loss'][-1])
            # if step % 10 == 0:
            # dqn_agent.save_model("trial-{}.model".format(trial))
        if step <= 100:
            print("Completed in trial {} with {} steps".format(trial, step))
            # print(params['losses'], dqn_agent.out.history['loss'][-1])
            # dqn_agent.save_model("success.model")
            # break
        if trial % 1 == 0:
            print("Logged no. {} trial with {} epsilon".format(str(trial), dqn_agents[0].epsilon))
            logger.save_end(envW.get_env(), acc_rewards)

    # return dqn_agent.out, dqn_agent.model

    print('Finished Training Session. Saving model and weights')
    trial = 'omega'
    dqn_agents[0].save_model("trial-{}.model".format(trial))

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
