import datetime
import logging.config
import os
import random
import uuid
import string


def setup_logging(path='config/logging.ini',
                  level=logging.INFO,
                  env_key='LOG_CFG'):
    log_file_path = os.getenv(env_key, path)
    if log_file_path and os.path.exists(log_file_path):
        logging.config.fileConfig(log_file_path)
    else:
        logging.basicConfig(level=level)


def get_uuid():
    return "urn:uuid:" + str(uuid.uuid4())


def get_random_alpha_numeric_string(length):
    return ''.join(random.choices(string.hexdigits, k=length))


def get_current_date_time_iso8601_format():
    strftime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
    strftime = strftime[:-3] + 'Z'
    return strftime

