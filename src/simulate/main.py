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


def main():
    utils.setup_logging()
    logging.info("Start Of Script")
    logging.info("Python version %s", sys.version)
    logging.info("OpenSSL version %s ", ssl.OPENSSL_VERSION)

    args = argparse.ArgumentParser()
    args.add_argument('property_files', help='path to the props.ini file')
    args.add_argument('directory_json_files', help='path to directory that contains json files')
    parse_args = args.parse_args()
    properties_filename = parse_args.property_files
    json_files_dir = parse_args.directory_json_files

    # trying to read the properties file which is a yaml file
    try:
        config_yml_stream = open(properties_filename, 'rb')
    except IOError as e:
        logging.error("Problem reading the file %s due to %s", properties_filename, e)
        sys.exit(1)
    with config_yml_stream:
        try:
            config_yml_obj = yaml.load(config_yml_stream)
        except YAMLError as e:
            logging.error("Problem loading the file %s due to %s", properties_filename, e)
            sys.exit(1)

    files = os.listdir(json_files_dir)
    logging.info("list of json files in the directory %s", files)
    for file in files:
        path_to_file = json_files_dir + "/" + file
        try:
            caliper_event = open(path_to_file, 'rb')
        except IOError as e:
            logging.error("cannot read the file %s due to %s", path_to_file, e)
            continue
        with caliper_event:
            event = caliper_event.read()
            try:
                jsonEvent = json.loads(event)
            except JSONDecodeError as e:
                logging.error("Failed to Deserialize the caliper event %s ", e)
                continue
            # make needed changes to the json events
            event_transformer = Transformer(jsonEvent, config_yml_obj)
            json_event_transformed = event_transformer.event_transformer()

            if json_event_transformed is None:
                logging.error("Problem in transforming a event Json")
                continue
            # sending to endpoint
            handler = HttpHandler(config_yml_obj)
            handler.make_api_call(json_event_transformed)
    logging.info("End Of Script")


if __name__ == "__main__":
    main()
