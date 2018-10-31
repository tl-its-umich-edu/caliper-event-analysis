from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import react
from requests_threads import AsyncSession
import json
from json import JSONDecodeError
import sys
import argparse
import os
import yaml
import utils
from yaml import YAMLError
import logging
from event_transformer.Transformer import Transformer
from main import get_transformed_event

args = argparse.ArgumentParser()
args.add_argument('property_files', help='path to the config.yml file')
args.add_argument('directory_json_files', help='path to directory that contains json files')
args.add_argument('parallel_threads', nargs='?', help='number representing how many times to send the static events',
                  type=int, default=1)
parse_args = args.parse_args()
properties_filename = parse_args.property_files
json_files_dir = parse_args.directory_json_files
no_threads = parse_args.parallel_threads
session = AsyncSession(n=no_threads)
utils.setup_logging()

@inlineCallbacks
def main(reactor):
    responses = []
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
    file=list(filter(lambda file: file.endswith(".json"), files))[0]
    path_to_file = json_files_dir + os.sep + file
    data=read_json(path_to_file)
    json_event_transformed = get_transformed_event(config_yml_obj, data)
    logging.info('Json data to be sent {} '.format(json_event_transformed))
    endpoint=config_yml_obj[utils.PROPS_ENDPOINT]

    url = endpoint[utils.PROPS_URL]
    token = endpoint[utils.PROPS_TOKEN]
    content_type = 'Content-type'
    authorization = 'Authorization'
    mime_type_json = 'application/json'
    bearer = 'Bearer '+token
    headers = {content_type: mime_type_json,authorization:bearer}
    for i in range(no_threads):
        responses.append(session.post(url,json=json_event_transformed, headers=headers))
    for response in responses:
        r = yield response
        logging.info('Response {} '.format(r))
    logging.info('no of concurrent events sents {} amd number of response received {} '.format(no_threads,len(responses)))

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

if __name__ == '__main__':
    react(main)