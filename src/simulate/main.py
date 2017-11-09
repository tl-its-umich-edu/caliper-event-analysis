#!/usr/bin/env python3

import sys
import argparse
import os
import logging
import utils
import ssl
import json
from json import JSONDecodeError
from event_transformer.Transformer import Transformer
from send_to_udp.HttpHandler import HttpHandler
import yaml
from yaml import YAMLError


def read_json(json_file_path):
    try:
        caliper_event = open(json_file_path, 'rb')
    except IOError as e:
        logging.error('cannot read the file %s due to %s', json_file_path, e)
        return None
    with caliper_event:
        event = caliper_event.read()
        try:
            json_event = json.loads(event)
        except JSONDecodeError as e:
            logging.error('Failed to Deserialize the caliper event %s', e)
            return None
    return json_event


def main():
    utils.setup_logging()
    logging.info('Start Of App')
    logging.info('Python version %s', sys.version)
    logging.info('OpenSSL version %s ', ssl.OPENSSL_VERSION)

    args = argparse.ArgumentParser()
    args.add_argument('property_files', help='path to the config.yml file')
    args.add_argument('directory_json_files', help='path to directory that contains json files')
    args.add_argument('times_to_run', nargs='?', help='number representing how many times to send the static events',
                      type=int, default=1)
    parse_args = args.parse_args()
    properties_filename = parse_args.property_files
    json_files_dir = parse_args.directory_json_files
    run_count = parse_args.times_to_run

    # trying to read the properties file which is a yaml file
    try:
        config_yml_stream = open(properties_filename, 'rb')
    except IOError as e:
        logging.error('Problem reading the file %s due to %s', properties_filename, e)
        sys.exit(1)
    with config_yml_stream:
        try:
            config_yml_obj = yaml.load(config_yml_stream)
        except YAMLError as e:
            logging.error('Problem loading the file %s due to %s', properties_filename, e)
            sys.exit(1)

    files = os.listdir(json_files_dir)
    logging.info('list of json files in the directory %s', files)
    for i in range(run_count):
        for file in files:
            if file.endswith(".json"):
                path_to_file = json_files_dir + "/" + file
                # Deserialize Json data
                json_event = read_json(path_to_file)
                if json_event is None:
                    continue
                # make needed changes to the json events
                event_transformer = Transformer(json_event, config_yml_obj)
                json_event_transformed = event_transformer.transformer()
                if json_event_transformed is None:
                    logging.error('Problem in transforming an event Json')
                    continue
                # sending to endpoint
                handler = HttpHandler(config_yml_obj)
                handler.make_api_call(json_event_transformed)
        logging.info('running count %s ', i + 1)

    logging.info('End Of App')


if __name__ == '__main__':
    main()
