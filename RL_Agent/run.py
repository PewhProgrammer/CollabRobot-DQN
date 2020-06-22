"""Startup module
"""

import sys
import config
from logic.trainer import Trainer
from containers.env_wrapper import EnvWrapper
from containers.gym_wrapper import CustomEnv
from containers.multi_agent_gym_wrapper import MultiAgentCustomEnv

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

import io_functions.game_logger as logger
import io_functions.serializer as serializer
import talos
import time


def baseline():
    config_name = config.small_narrow_passages_single
    for i in range(5):
        train_single("models/single_dqn_transport_v3", config_name,  500000)
    # train_multiple("models/tmp_multi_agent_model", 80000)

    test_phase(config_name)


def train_single(model_name, config_name, total_timesteps,  load_model=None):
    gym_wrapper = CustomEnv(config_name)
    if load_model is None:
        model = DQN(MlpPolicy, gym_wrapper, verbose=1,
                    double_q=True,
                    prioritized_replay=True,
                    policy_kwargs=dict(dueling=True),
                    tensorboard_log="./study/algorithm_test/concept-1/small_narrow/")
    else:
        model = DQN.load("models/single_dqn_transport", env=gym_wrapper)

    model.learn(total_timesteps=total_timesteps, tb_log_name="gradient_ddp_experiment")
    model.save(model_name)


def train_multiple(model_name, total_timesteps):
    gym_wrapper = CustomEnv(config.small_room_single)
    model_trained = DQN.load("models/single_dqn_transport", env=gym_wrapper)
    gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)
    model = DQN(MlpPolicy, gym_wrapper, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    model.save(model_name)

    del model  # remove to demonstrate saving and loading


def test_phase(config_name):
    # model_trained = DQN.load("models/single_dqn_transport", env=CustomEnv(config.small_room_single))
    # gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)

    gym_wrapper = CustomEnv(config_name)
    model = DQN.load("models/single_dqn_transport_v3.zip", env=gym_wrapper)

    step = 0
    episode = 0
    acc_rewards = 0

    logger.save_init(gym_wrapper.get_env())
    obs = gym_wrapper.input_data(0)

    ep_stats = {}

    while episode < 150:

        step += 1
        action, _states = model.predict(obs)
        obs, rewards, done, info = gym_wrapper.step(action)
        acc_rewards += rewards

        logger.save_state(gym_wrapper.get_env(), "E" + str(episode) + "_S" + str(step))
        if done:
            env = gym_wrapper.get_env()
            print("[E-{}] Accumulated rewards: {}".format(episode, acc_rewards))
            finished = env.objective_manager.is_done()

            logger.save_end(env, acc_rewards, finished)
            ep_stats[episode] = (acc_rewards, finished)
            gym_wrapper.reset()
            logger.save_init(env)

            step = 0
            episode += 1
            acc_rewards = 0

    f = open("study/algorithm_test/double_dueling_prioritized/eval-150-cross.log", "w")
    f.write(serializer.export_dict_to_string("E{}".format(ep_stats)))
    f.close()


def main(args):
    # create evironment
    gym_wrapper = CustomEnv(config.small_room_single_test)
    trainer = Trainer(gym_wrapper, None)
    trainer.learn(timesteps=10000)

def apply_study():
    x, y = talos.templates.datasets.iris()

    def dqn(x_train, y_train, x_val, y_val, params):
        # create evironment
        gym_wrapper = CustomEnv(config.small_room_single_test)
        trainer = Trainer(gym_wrapper, params=config.default)
        return trainer.learn(timesteps=100000)

    # NOTE: clear session prevents using too much memory, save_weights does not save each model, can also save memory
    scan_object = talos.Scan(x, y, model=dqn, params=config.talos_params, experiment_name='study',
                             fraction_limit=0.5, clear_session=True, save_weights=False)
    return scan_object


if __name__ == '__main__':
    start_time = time.perf_counter()

    # main(parse_arguments(sys.argv[1:]))
    baseline()

    elapsed_time = time.time() - start_time
    time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
