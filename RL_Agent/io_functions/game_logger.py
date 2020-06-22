import os
import logging
import io_functions.serializer as util
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

datetime.today().strftime('%Y-%m-%d')

filename = 'data\\session_{0}\\time-{1}.log'.format(datetime.today().strftime('%d.%m'), datetime.today().strftime('%H%M'))
os.makedirs(os.path.dirname(filename), exist_ok=True)

# create a file handler
handler = logging.FileHandler(filename, 'w+')
handler.setLevel(logging.INFO)

# create a logging format
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# add the file handler to the logger
logger.addHandler(handler)

start = {}
body = []


def save_state(env, state_id):
    # logger.info(util.export_state(env, state_id))
    body.append(util.export_state(env, state_id))


def save_end(env, acc_rewards, completed=False):
    global start, body
    payload = util.export_end_state(env, acc_rewards, completed)
    # print("Accumulated rewards: {}".format(acc_rewards))

    # merge every struct into result
    result = {**start, **{'games': body}}
    result = {**result, **payload}

    logger.info(util.export_dict_to_string(result))  # save into file
    # print("Accumulated rewards: {}".format(result["acc_rewards"]))

    # reset containers
    start = {}
    body = []


def save_init(env):
    global start
    # start.update(["init", util.export_start_state(env)])
    # logger.info(util.export_start_state(env))

    start = {**start, **util.export_start_state(env)}


def log(msg):
    logger.info(msg)
