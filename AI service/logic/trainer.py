"""Core ML module for predicting the next move of the robots
"""

from routes import render_env
import io_functions.game_logger as logger

from logic.DQN import DQN


def game_loop(envW, sio=None, params=None):
    trials = params['epochs']
    trial_len = 200

    # updateTargetNetwork = 1000
    dqn_agent = DQN(env=envW, params=params)
    steps = []
    step = 0

    for trial in range(trials):
        cur_state = envW.reset(trial)
        acc_rewards = 0
        logger.save_init(envW.get_env())
        for step in range(trial_len):
            identifier = "E" + str(envW.get_env().episode) + "_S" + str(step)
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = envW.step(action)
            acc_rewards += reward

            # reward = reward if not done else -20
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            dqn_agent.replay()  # internally iterates default (prediction) model
            dqn_agent.target_train()  # iterates target model

            # render_env(sio)
            logger.save_state(envW.get_env(), identifier)

            cur_state = new_state
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

    return dqn_agent.out, dqn_agent.model

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# print(tf.reduce_sum(tf.random.normal([1000, 1000])))
