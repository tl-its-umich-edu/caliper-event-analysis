import logging
import requests
import utils
import time


class HttpHandler:
    def __init__(self, config_data, session):
        self.config_data = config_data
        self.session = session

    def make_api_call(self, data):
        response = None
        try:
            endpoint = self.config_data[utils.PROPS_ENDPOINT]
        except KeyError:
            logging.error('configuration yaml is missing the \"' + utils.PROPS_ENDPOINT + '\" key')
            return
        if endpoint is None or endpoint['url'] is None or endpoint['token'] is None:
            logging.error('End Point information not available to the configuration yml file')
            return
        url = endpoint[utils.PROPS_URL]
        token = endpoint[utils.PROPS_TOKEN]
        mime_type_json = 'application/json'
        content_type = 'Content-type'
        authorization = 'Authorization'
        bearer = 'Bearer '+token
        headers = {content_type: mime_type_json,authorization:bearer}
        try:
            start = time.time()
            response = self.session.post(url, json=data, headers=headers, stream=True, timeout=(3.05,0.00001))
        except (requests.exceptions.RequestException, Exception) as e:
            logging.error('Connection to endpoint failed %s\n' % e)
        end = time.time()
        logging.info('it took about {} sec to get response from UDP' .format(round(end-start,3)))
        # return response
