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
import requests
from datetime import timedelta
import time
from time import sleep


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
            logging.error('Deserializing the caliper event in the path %s failed due to:  %s', json_file_path, e)
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
    session = requests.session()
    logging.info('list of json files in the directory %s', files)
    event_count = 0
    delay_in_ms = utils.add_milli_sec_delay()
    os.environ["TZ"]="US/Eastern"
    time.tzset()
    start = time.time()
    for i in range(run_count):
        for file in filter(lambda file: file.endswith(".json"), files):
            path_to_file = json_files_dir + os.sep + file
            # Deserialize Json data
            json_event = read_json(path_to_file)
            if json_event is None:
                continue
            # make needed changes to the json events
            json_event_transformed = get_transformed_event(config_yml_obj, json_event)
            if json_event_transformed is None:
                logging.error('Problem in transforming an event Json')
                continue
            # sending to endpoint
            sleep(delay_in_ms)
            event_count = send_to_udp(config_yml_obj, json_event_transformed, session, event_count)
        logging.info('running count %s ', i + 1)
        # only print every tenth event
        # if divmod(event_count, 10)[1] == 0:
        logging.info('so far {} events are sent '.format(event_count))
    end=time.time()
    elapsed = end - start
    logging.info('StartTime: ({}) and EndTime: ({})'.format(time.strftime("%D %T %Z", time.localtime(start)), time.strftime("%D %T %Z", time.localtime(end))))
    logging.info('Total {} events sent to UDP in {} and successful run will send {} events'.format(event_count,
                                                                                                   timedelta(
                                                                                                       seconds=elapsed)
                                                                                                   , run_count * get_json_file_count(
            files)))
    logging.info('End Of App')

def get_json_file_count(files):
    count = 0
    for file in filter(lambda file: file.endswith(".json"), files):
        count+=1
    return count


def get_transformed_event(config_yml_obj, json_event):
    event_transformer = Transformer(json_event, config_yml_obj)
    json_event_transformed = event_transformer.transformer()
    return json_event_transformed


def send_to_udp(config_yml_obj, json_event_transformed, session, count):
    handler = HttpHandler(config_yml_obj, session)
    handler.make_api_call(json_event_transformed)
    # if response is None:
    #     return count
    # if response.status_code != requests.codes.ok:
    #     logging.error('sending data to endpoint failed with status code %s due to %s ', response.status_code,
    #                   response.text)
    #     return count
    # we increment the count on successful response
    count += 1
    # logging.debug('Success in sending the event to Endpoint' + response.text)
    return count


if __name__ == '__main__':
    main()
