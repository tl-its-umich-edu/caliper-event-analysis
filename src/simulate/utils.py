import logging.config
import os


def setup_logging(path='config/logging.ini',
                  level=logging.INFO,
                  env_key='LOG_CFG'):
    log_file_path = os.getenv(env_key, path)
    if log_file_path and os.path.exists(log_file_path):
        logging.config.fileConfig(log_file_path)
    else:
        logging.basicConfig(level=level)
