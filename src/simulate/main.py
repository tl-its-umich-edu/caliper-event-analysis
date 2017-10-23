#!/usr/bin/env python3

import sys
import argparse
import configparser
import os
import logging
import utils
import ssl
from event_transformer import Transformer
from send_to_udp import HttpHandler


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

    # reading the configuration file
    config = configparser.ConfigParser()
    config.read(properties_filename)
    url = config.get("oauth", "url")
    if not bool(url):
        logging.error("Endpoint url is not provided in props.ini file")
        sys.exit(1)
    logging.info("End Point URL %s", url)
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
            # make needed changes to the json events
            event_transformer = Transformer(event)
            json_event_transformed = event_transformer.event_transformer()
            # sending it to endpoint
            if json_event_transformed is None:
                logging.error("Problem in transforming a event Json")
                continue
            handler = HttpHandler(url)
            handler.make_api_call(json_event_transformed)
    logging.info("End Of Script")


if __name__ == "__main__":
    main()
