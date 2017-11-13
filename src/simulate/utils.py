from datetime import datetime, timedelta
import logging.config
import os
import random
import uuid
import string
import yaml
from random import randint
from os import environ


PROPS_USER_ID = 'id'
PROPS_USER_SIS_ID = 'user_sis_id'
PROPS_USER_CANVAS_ID = 'user_canvas_id'
PROPS_COURSE_SITE = 'course_site'
PROPS_COURSE_NAME = 'course_name'
PROPS_COURSE_SIS_ID = 'course_sis_id'
PROPS_COURSE_CANVAS_ID = 'course_canvas_id'
PROPS_VIDEO_PLAYER = 'video_player'
PROPS_COURSES = 'courses'
PROPS_USERS = 'users'
PROPS_ENDPOINT = 'endpoint'
PROPS_URL = 'url'
PROPS_PLAYER_NAME = 'player_name'
OPEN_SHIFT_ENV_LOGGING_LEVEL = 'LOGGING_LEVEL'


def setup_logging(path='config/logging.yml',
                  env_key='LOG_CFG'):
    os_env_log_level = environ.get(OPEN_SHIFT_ENV_LOGGING_LEVEL)
    if os_env_log_level is None:
        # load the logging level from the file
        logging_config_from_file(env_key, path)
    else:
        # App is running from OpenShift so logging level is set as part of environmental variable
        logging_config_from_env_variable()


def logging_config_from_env_variable():
    logging_level = os.environ[OPEN_SHIFT_ENV_LOGGING_LEVEL]
    if logging_level is None:
        # set it to INFO if missed when running the POD
        logging.basicConfig(logging.INFO)
        logging.info("Logging level is set from basic config")

    logging_level = logging_level.upper()
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.getLevelName(logging_level))
    logging.info("Logging level is set from OpenShift Environmental variable")


def logging_config_from_file(env_key, path):
    log_file_path = os.getenv(env_key, path)
    if log_file_path and os.path.exists(log_file_path):
        with open(log_file_path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)
            logging.info("Logging level is set from logging.yml")
    else:
        logging.basicConfig(logging.INFO)
        logging.info("Logging is configured from basic config and default to INFO")


def get_uuid():
    return "urn:uuid:" + str(uuid.uuid4())


def get_random_alpha_numeric_string(length):
    return ''.join(random.choices(string.hexdigits, k=length))


def get_current_date_time_iso8601_format():
    iso_utc_now = (datetime.utcnow() + timedelta(seconds=random.randint(1, 9))).strftime('%Y-%m-%dT%H:%M:%S.%f')
    iso_utc_now = iso_utc_now[:-3] + 'Z'
    return iso_utc_now


# returns a random n digit number
def random_number_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


# this will generate a floating point number between the range [0,n]
def get_random_floating_point_number(n):
    return '{:04.3f}'.format(random.uniform(0, n))
