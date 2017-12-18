import logging
import requests
import utils


class HttpHandler:
    def __init__(self, config_data):
        self.config_data = config_data

    def make_api_call(self, data):
        response = None
        try:
            endpoint = self.config_data[utils.PROPS_ENDPOINT]
        except KeyError:
            logging.error('configuration yaml is missing the\"' + utils.PROPS_ENDPOINT + '\"key')
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
            response = requests.post(url, json=data, headers=headers)
        except (requests.exceptions.RequestException, Exception) as e:
            logging.error('Connection to endpoint failed %s\n' % e)
            return response

        if response.status_code != requests.codes.ok:
            logging.error('sending data to endpoint failed with status code %s due to %s ', response.status_code,
                          response.text)
        logging.info('text: '+response.text)
        logging.info('binary content: '+str(response.content))
        logging.info('Json reposne '+str(response.json()))
        logging.info('Raw response '+str(response.raw))
        logging.debug('Success in sending the event to Endpoint')
        return response
