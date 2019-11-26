"""Startup module
"""

import sys
import argparse
from routes import init_flask_app
from logic.predictor import init_predictor, run_prediction


def main(args):
    # print(args)
    # default()
    pickup_example()
    sio_context = init_flask_app()
    run_prediction(sio_context)
    sio_context.sleep(5)


def pickup_example():
    config = {
        "id": 1,
        "width": 10,
        "height": 10,
        "agents": 1,
        "agentPosX": 5,
        "agentPosY": 5,
        "pickupX": 2,
        "pickupY": 5,
        "dropoffX": 8,
        "dropoffY": 5
    }
    init_predictor(config)


def default():
    config = {
        "id": 0,
        "width": 20,
        "height": 20,
        "agents": 1
    }
    init_predictor(config)


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
