"""Startup module
"""

import sys
import config
from logic.predictor import run_prediction
from containers.env_wrapper import EnvWrapper

import talos


def apply_study():
    x, y = talos.templates.datasets.iris()

    def dqn(x_train, y_train, x_val, y_val, params):
        # create evironment
        envWrap = EnvWrapper(config.map_5x5)
        return run_prediction(envWrap, params=params)

    # NOTE: clear session prevents using too much memory, save_weights does not save each model, can also save memory
    scan_object = talos.Scan(x, y, model=dqn, params=config.talos_params, experiment_name='study',
                             fraction_limit=0.5, clear_session=True, save_weights=False)
    return scan_object


def main(args):
    # create evironment
    envWrap = EnvWrapper(config.map_5x5)

    # apply_study()

    # sio_context = init_flask_app(envWrap)
    run_prediction(envWrap, params=config.default)
    # sio_context.sleep(5)


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


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
