"""Startup module
"""

import config
from logic.trainer import Trainer
from containers.env_wrapper import EnvWrapper
from containers.gym_wrapper import CustomEnv
from containers.multi_agent_gym_wrapper import MultiAgentCustomEnv

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

import io_functions.game_logger as logger
from timeit import default_timer as timer
from datetime import timedelta


def baseline():
    config_name = config.small_room_single_test
    for i in range(2):
        i += 3
        train_single(config.small_room_single, i)
        test_phase(config.small_room_single_test, i)

    for i in range(5):
        train_single(config.normal_room_single, i)
        test_phase(config.normal_room_single_test, i)

    # train_multiple("models/tmp_multi_agent_model", 80000)


def train_single(cfg, version, load_model=None):
    gym_wrapper = CustomEnv(cfg)
    if load_model is None:
        model = DQN(MlpPolicy, gym_wrapper, verbose=1,
                    double_q=cfg["double-dqn"],
                    prioritized_replay=cfg["prioritized"],
                    policy_kwargs=dict(dueling=cfg["dueling"]),
                    tensorboard_log=cfg["study_results"] + "tensorboard/")
    else:
        model = DQN.load("{}models/single_dqn_transport".format(cfg["study_results"]), env=gym_wrapper)

    model.learn(total_timesteps=cfg["timesteps"], tb_log_name=cfg["experiment_name"])
    model.save("{0}models/{2}-v{1}".format(cfg["study_results"], version, cfg["experiment_name"]))


def train_multiple(model_name, total_timesteps):
    gym_wrapper = CustomEnv(config.small_room_single)
    model_trained = DQN.load("models/single_dqn_transport", env=gym_wrapper)
    gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)
    model = DQN(MlpPolicy, gym_wrapper, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    model.save(model_name)

    del model  # remove to demonstrate saving and loading


def test_phase(config_name, version):
    # model_trained = DQN.load("models/single_dqn_transport", env=CustomEnv(config.small_room_single))
    # gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)

    gym_wrapper = CustomEnv(config_name)
    model = DQN.load("{0}models/{2}-v{1}".format(config_name["study_results"], version, config_name["experiment_name"]),
                     env=gym_wrapper)

    step = 0
    episode = 0
    acc_rewards = 0
    completed = 0

    logger.create_new_handler(config_name["study_results"], config_name["experiment_name"])
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
            if finished:
                completed += 1
            gym_wrapper.reset()
            logger.save_init(env)

            step = 0
            episode += 1
            acc_rewards = 0

    # append end state information to log file

    print("Completion rate: {}".format(completed / episode))
    config_name["completion"] = completed / episode
    logger.log_json(config_name)
    # f = open("study/algorithm_test/eval-150-cross.log", "w") f.write(serializer.export_dict_to_string("E{}".format(
    # ep_stats))) # use this to store all reward and completion episodes f.close()


def main(args):
    # create evironment
    gym_wrapper = CustomEnv(config.small_room_single_test)
    trainer = Trainer(gym_wrapper, None)
    trainer.learn(timesteps=10000)


if __name__ == '__main__':
    start = timer()

    # main(parse_arguments(sys.argv[1:]))
    baseline()

    end = timer()
    print("Elapsed time: {}".format(timedelta(seconds=end - start)))
