"""Startup module
"""

import config
from logic.trainer import game_loop
from containers.env_wrapper import EnvWrapper
from containers.gym_wrapper import CustomEnv
from containers.multi_agent_gym_wrapper import MultiAgentCustomEnv

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

import io_functions.game_logger as logger
import talos


def baseline():
    # train_single("models/single_dqn_transport", 15000)
    train_multiple("models/tmp_multi_agent_model", 80000)

    model_trained = DQN.load("models/single_dqn_transport", env=CustomEnv(config.small_room_single))
    gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)

    test_phase(
        gym_wrapper,
        DQN.load("models/tmp_multi_agent_model", env=gym_wrapper))


def train_single(model_name, total_timesteps):
    gym_wrapper = CustomEnv(config.small_room_single)
    model = DQN(MlpPolicy, gym_wrapper, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    model.save(model_name)


def train_multiple(model_name, total_timesteps):
    gym_wrapper = CustomEnv(config.small_room_single)
    model_trained = DQN.load("models/single_dqn_transport", env=gym_wrapper)
    gym_wrapper = MultiAgentCustomEnv(config.small_room_p2_multiple, model_trained)
    model = DQN(MlpPolicy, gym_wrapper, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    model.save(model_name)

    del model  # remove to demonstrate saving and loading

def test_phase(gym_wrapper, model):
    step = 0
    episode = 0
    acc_rewards = 0

    logger.save_init(gym_wrapper.get_env())
    obs = gym_wrapper.reset()

    while episode < 25:

        step += 1
        action, _states = model.predict(obs)
        obs, rewards, dones, info = gym_wrapper.step(action)
        acc_rewards += rewards

        logger.save_state(gym_wrapper.get_env(), "E" + str(episode) + "_S" + str(step))
        if dones:
            print("[E-{}] Accumulated rewards: {}".format(episode, acc_rewards))
            logger.save_end(gym_wrapper.get_env(), acc_rewards)
            logger.save_init(gym_wrapper.get_env())
            gym_wrapper.reset()
            step = 0
            episode += 1
            acc_rewards = 0


def main(args):
    # create evironment
    envWrap = EnvWrapper(config.small_room)
    # apply_study()
    game_loop(envWrap, params=config.default)


def parse_arguments(argv):
    # parser = argparse.ArgumentParser()

    # parser.add_argument('mode', type=str, choices=['TRAIN', 'CLASSIFY'],
    #     help='Indicates if a new classifier should be trained or a classification ' + 
    #     'model should be used for classification', default='CLASSIFY')
    # parser.add_argument('data_dir', type=str,
    #     help='Path to the data directory containing aligned LFW face patches.')
    # parser.add_argument('model', type=str, 
    #     help='Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    # parser.add_argument('classifier_filename', 
    #     help='Classifier model file name as a pickle (.pkl) file. ' + 
    #     'For training this is the output and for classification this is an input.')
    # parser.add_argument('--use_split_dataset', 
    #     help='Indicates that the dataset specified by data_dir should be split into a training and test set. ' +  
    #     'Otherwise a separate test set can be specified using the test_data_dir option.', action='store_true')
    # parser.add_argument('--test_data_dir', type=str,
    #     help='Path to the test data directory containing aligned images used for testing.')
    # parser.add_argument('--batch_size', type=int,
    #     help='Number of images to process in a batch.', default=90)
    # parser.add_argument('--image_size', type=int,
    #     help='Image size (height, width) in pixels.', default=160)
    # parser.add_argument('--seed', type=int,
    #     help='Random seed.', default=666)
    # parser.add_argument('--min_nrof_images_per_class', type=int,
    #     help='Only include classes with at least this number of images in the dataset', default=20)
    # parser.add_argument('--nrof_train_images_per_class', type=int,
    #     help='Use this number of images from each class for training and the rest for testing', default=10)

    # return parser.parse_args(argv)

    return argv


def apply_study():
    x, y = talos.templates.datasets.iris()

    def dqn(x_train, y_train, x_val, y_val, params):
        # create evironment
        envWrap = EnvWrapper(config.map_5x5)
        return game_loop(envWrap, params=params)

    # NOTE: clear session prevents using too much memory, save_weights does not save each model, can also save memory
    scan_object = talos.Scan(x, y, model=dqn, params=config.talos_params, experiment_name='study',
                             fraction_limit=0.5, clear_session=True, save_weights=False)
    return scan_object


if __name__ == '__main__':
    # main(parse_arguments(sys.argv[1:]))
    baseline()
