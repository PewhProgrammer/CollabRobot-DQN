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
from io_functions.serializer import export_dict_to_string

import os


def baseline():
    for i in range(5):
        # sensor test
        # train_single(config.small_warehouse_single, i)
        # test_phase(config.small_warehouse_single_test, i)

        for i in range(5):
            run_config(config.wide_room_single, config.wide_room_single_test
                       , "reward_conf", [0, 5, 0, 15, -15, 0], "experiment_sparse", i)

        for i in range(5):
            run_config(config.wide_room_single, config.wide_room_single_test
                       , "reward_conf", [0, 5, 0, 15, -15, -0.25], "experiment_negative", i)

        for i in range(5):
            run_config(config.wide_room_single, config.wide_room_single_test
                       , "reward_conf", [0.05, 150, 10, 2000, 0, 0], "experiment_gradient", i)

        # run_config(config.small_warehouse_single, config.small_warehouse_single_test
        #          , "sensor_information", True, "test_pf1_p10_d2000_t2mil_pow0'4_pSolid_sensor", i)

    # train_multiple("models/tmp_multi_agent_model", 80000)


def run_task_allocation(cfg, cfg_test, runs=20):
    best_completion = 0
    best_params = []

    param = [2, 14, 14, 2000, -100, 0]
    for i in range(runs):
        tmp_completion = run_config(cfg, cfg_test
                                    , "reward_conf", param,
                                    "allocation_test"
                                    , i, mode="task_allocation",
                                    model_name="best/allocation_best")

        if tmp_completion > best_completion:
            best_completion = tmp_completion
            best_params = i

    print("The best completion was {0} at run {1}".format(best_completion, best_params))


def run_reward_function(cfg, cfg_test, runs=20):
    change_config(cfg, cfg_test,
                  "study_results", "./study/algorithm_test/larger_env/wide_room/")

    # for i in range(runs):
    #     run_config(cfg, cfg_test
    #                , "reward_conf", [0, 150, 0, 2000, -15, 0], "experiment_1mil_sparse", i)
    #
    # for i in range(runs):
    #     run_config(cfg, cfg_test
    #                , "reward_conf", [0, 150, 0, 2000, -15, -0.25], "experiment_1mil_negative", i)

    for i in range(runs):
        run_config(cfg, cfg_test
                   , "reward_conf", [0.05, 150, 10, 2000, 0, 0], "experiment_1mil_gradient", i)


def run_double_dueling_prioritized(runs=20):
    # every variant is turned on
    for i in range(runs):
        train_single(config.normal_room_single, i)
        test_phase(config.normal_room_single_test, i)

    for i in range(runs):
        run_config(config.normal_room_single, config.normal_room_single_test
                   , "prioritized", False, "experiment_double-dueling", i)

    change_config(config.normal_room_single, config.normal_room_single_test, "prioritized", True)

    for i in range(runs):
        run_config(config.normal_room_single, config.normal_room_single_test
                   , "dueling", False, "experiment_double-prioritized", i)

    change_config(config.normal_room_single, config.normal_room_single_test, "dueling", True)

    for i in range(runs):
        run_config(config.normal_room_single, config.normal_room_single_test
                   , "double-dqn", False, "experiment_dueling-prioritized", i)


def run_sensor(cfg, cfg_test, runs=20):
    # test without sensors
    # for i in range(runs):
    #     run_config(cfg, cfg_test
    #                , "reward_conf", [0.05, 150, 10, 2000, 0, 0], "experiment_gradient", i)

    change_config(cfg, cfg_test
                  , "reward_conf", [0.05, 150, 10, 2000, 0, 0])

    # test with sensors
    for i in range(runs):
        run_config(cfg, cfg_test
                   , "sensor_information", False, "experiment_gradient_sensorOFF", i)


def run_collaboration(cfg, cfg_test, runs=20):
    best_completion = 0
    best_params = []

    # tmp_completion, param = run_hyperparameter_test(cfg, cfg_test, [0, 5, 0.5], runs, 0, "p_reward")
    # if tmp_completion > best_completion:
    #     best_completion = tmp_completion
    #     best_params = param
    # tmp_completion, param = run_hyperparameter_test(cfg, cfg_test, [0, 20, 1], runs, 1, "p_reward_final")
    # if tmp_completion > best_completion:
    #     best_completion = tmp_completion
    #     best_params = param
    # tmp_completion, param = run_hyperparameter_test(cfg, cfg_test, [0, 20, 1], runs, 2, "d_reward")
    # if tmp_completion > best_completion:
    #     best_completion = tmp_completion
    #     best_params = param
    # tmp_completion, param = run_hyperparameter_test(cfg, cfg_test, [0, 4000, 400], runs, 3, "p_reward_final")
    # if tmp_completion > best_completion:
    #     best_completion = tmp_completion
    #     best_params = param
    param = [1, 35, 10, 2000, -14, 0]
    for i in range(runs):
        tmp_completion = run_config(cfg, cfg_test
                                    , "reward_conf", param,
                                    "collab_single_proto"
                                    , i, mode="task_allocation",
                                    model_name="best_models/collab_single_bad")
        # model_name="best_models/collab_multiple_best-v0")

        if tmp_completion > best_completion:
            best_completion = tmp_completion
            best_params = i

    print("The best completion was {0} at run {1}".format(best_completion, best_params))


def run_hyperparameter_test(cfg, cfg_test, interval, runs, parameter, parameter_name):
    best_completion = 0
    best_params = []
    change_config(cfg, cfg_test
                  , "reward_conf", [1, 150, 10, 2000, 0, 0])

    # hyperparameter check: p_reward_final
    pun = interval[0]
    while pun < interval[1]:
        # [interval0, interval1]
        pun = round(pun + interval[2], 1)  # steps are interval[2]
        param = [1, 10, 10, 2000, 0, 0]
        param[parameter] = pun
        for i in range(runs):
            completion_rate = run_config(cfg, cfg_test
                                         , "reward_conf", param,
                                         "collab_multiple_" + parameter_name
                                         , i, mode="multiple",
                                         model_name="collab_single_best")

            if completion_rate > best_completion:
                print("saved completion " + str(completion_rate))
                best_completion = completion_rate
                best_params = param

    return best_completion, best_params


def run_dynamic_hindrances(cfg, cfg_test, runs=20):
    # for j in range(10):
    #     pun = round((j + 1) * 0.1, 1)
    #     for i in range(runs):
    #         run_config(cfg, cfg_test
    #                    , "reward_conf", [1, 10, 10, 2000, pun, 0], "experiment_nosensor_punish_-" + str(pun), i)

    # change to sensorON

    change_config(cfg, cfg_test, "sensor_information", True)

    for i in range(runs):
        run_config(cfg, cfg_test
                   , "reward_conf", [1, 35, 1, 200, -15, 0], "experiment_", i)


def train_single(cfg, version, load_model=None):
    gym_wrapper = CustomEnv(cfg)
    if load_model is None:
        model = DQN(MlpPolicy, gym_wrapper, verbose=1,
                    double_q=cfg["double-dqn"],
                    prioritized_replay=cfg["prioritized"],
                    policy_kwargs=dict(dueling=cfg["dueling"]),
                    exploration_fraction=cfg["exploration_frac"],
                    tensorboard_log=cfg["study_results"] + "tensorboard/experiments/")
    else:
        model = DQN.load("{}models/single_dqn_transport".format(cfg["study_results"]), env=gym_wrapper)

    model.learn(total_timesteps=cfg["timesteps"], tb_log_name=cfg["experiment_name"])
    model.save("{0}models/{2}-v{1}".format(cfg["study_results"], version, cfg["experiment_name"]))


def train_multiple(cfg, version, trained_model, double_agent=False):
    # double_agent refers to both agents having learned in multi environment
    if double_agent:
        gym_wrapper = MultiAgentCustomEnv(cfg)
        # model_trained = DQN.load("{0}models/{1}".format("./", trained_model), env=gym_wrapper)
        model_trained = DQN.load("{0}models/{1}".format(cfg["study_results"], trained_model), env=gym_wrapper)
    else:
        gym_wrapper = CustomEnv(cfg)
        # model_trained = DQN.load("{0}models/{1}".format("./", trained_model), env=gym_wrapper)
        model_trained = DQN.load("{0}models/{1}".format(cfg["study_results"], trained_model), env=gym_wrapper)

    gym_wrapper = MultiAgentCustomEnv(cfg, model_trained, single=not double_agent)

    model = DQN(MlpPolicy, gym_wrapper, verbose=1,
                double_q=cfg["double-dqn"],
                prioritized_replay=cfg["prioritized"],
                policy_kwargs=dict(dueling=cfg["dueling"]),
                exploration_fraction=cfg["exploration_frac"],
                tensorboard_log=cfg["study_results"] + "tensorboard/experiments/")

    model.learn(total_timesteps=cfg["timesteps"], tb_log_name=cfg["experiment_name"])
    model.save("{0}models/{2}-v{1}".format(cfg["study_results"], version, cfg["experiment_name"]))


def test_phase(config_name, version, trained_model=None, multi=False, double_agent=False):
    if double_agent:
        gym_wrapper = MultiAgentCustomEnv(config_name)
        # model_trained = DQN.load("{0}models/{1}".format("./", trained_model), env=gym_wrapper)
        model_trained = DQN.load("{0}models/{1}".format(config_name["study_results"], trained_model), env=gym_wrapper)
        gym_wrapper = MultiAgentCustomEnv(config_name, model_trained, single=False)
    elif multi:
        gym_wrapper = CustomEnv(config_name)
        model_trained = DQN.load("{0}models/{1}".format(config_name["study_results"], trained_model), env=gym_wrapper)
        gym_wrapper = MultiAgentCustomEnv(config_name, model_trained)
    else:
        gym_wrapper = CustomEnv(config_name)

    model = DQN.load("{0}models/{2}-v{1}".format(config_name["study_results"], version, config_name["experiment_name"]),
                     env=gym_wrapper)

    step = 0
    episode = 0
    acc_rewards = 0
    completed = 0
    collided = 0
    min_steps_needed = 0
    steps_performed = 0


    logger.create_new_handler(config_name["study_results"], config_name["experiment_name"], version)
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

            logger.save_end(env, acc_rewards, finished, env.min_steps_to_completion, max(env.agents_moved_count,env.min_steps_to_completion))
            ep_stats[episode] = (acc_rewards, finished, env.min_steps_to_completion, env.agents_moved_count)
            if finished:
                completed += 1
                if env.get_agent().is_collided():
                    collided += 1

            min_steps_needed += env.min_steps_to_completion
            steps_performed += env.agents_moved_count

            gym_wrapper.reset()
            logger.save_init(env)

            step = 0
            episode += 1
            acc_rewards = 0

    # append end state information to log file

    print("Completion rate: {}".format(completed / episode))
    print("Collision rate: {}".format(collided / episode))
    config_name["completion"] = completed / episode
    config_name["collided"] = collided / episode
    if config_name["distance_information"]:
        print("Minimum steps: {0}  Performed steps: {1}".format(min_steps_needed , steps_performed))
        config_name["steps_surplus_rate"] = steps_performed / min_steps_needed
    logger.log_json(config_name)

    # use this to store all reward and completion episodes
    # f = open("study/algorithm_test/eval-150-performed-steps.log", "w")
    # f.write(export_dict_to_string("E{}".format(ep_stats)))
    # f.close()

    return config_name["completion"]


def run_config(cfg, cfg_test, key, value, name, version, mode="single", model_name=""):
    change_config(cfg, cfg_test, key, value)
    cfg["experiment_name"] = name
    cfg_test["experiment_name"] = name

    if mode == "multiple":
        change_config(cfg, cfg_test, "agents", 2)
        change_config(cfg, cfg_test, "p_weight", 2)
        change_config(cfg, cfg_test, "sensor_information", True)
        change_config(cfg, cfg_test, "study_results", "./study/algorithm_test/concept-4/small_room/")
        train_multiple(cfg, version, model_name, double_agent=False)
        return test_phase(cfg_test, version, trained_model=model_name, multi=True, double_agent=False)
    elif mode == "task_allocation":
        change_config(cfg, cfg_test, "agents", 2)
        change_config(cfg, cfg_test, "p_weight", 1)
        change_config(cfg, cfg_test, "distance_information", True)
        change_config(cfg, cfg_test, "study_results", "./study/algorithm_test/concept-3/small_room/")

        train_multiple(cfg, version, model_name)
        return test_phase(cfg_test, version=version, trained_model=model_name, multi=True, double_agent=True)
    else:
        train_single(cfg, version)
        return test_phase(cfg_test, version)


def change_config(cfg, cfg_test=None, key=None, value=None):
    cfg[key] = value
    if cfg_test is not None:
        cfg_test[key] = value


def main(args):
    # create evironment
    gym_wrapper = CustomEnv(config.small_room_single_test)
    trainer = Trainer(gym_wrapper, None)
    trainer.learn(timesteps=10000)


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    start = timer()

    # main(parse_arguments(sys.argv[1:]))
    # baseline()
    # run_double_dueling_prioritized(runs=15)
    # run_reward_function(config.wide_room_single, config.wide_room_single_test, runs=20)
    # run_sensor(config.wide_room_single, config.wide_room_single_test, runs=1)

    # run_dynamic_hindrances(config.small_room_single, config.small_room_single_test, runs=1)
    run_dynamic_hindrances(config.obstacle_lane, config.obstacle_lane_test, runs=1)
    # run_task_allocation(config.small_room_single, config.small_room_single_test, runs=1)
    # run_collaboration(config.small_room_single, config.small_room_single_test, runs=2)

    end = timer()
    print("Elapsed time: {}".format(timedelta(seconds=end - start)))
