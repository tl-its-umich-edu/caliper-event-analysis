import logging
import requests


class HttpHandler:
    def __init__(self, url):
        self.url = url

    def make_api_call(self, data):
        mime_type_json = 'application/json'
        content_type = 'Content-type'
        headers = {content_type: mime_type_json}
        response = None
        try:
            response = requests.post(self.url, json=data, headers=headers)
        except (requests.exceptions.RequestException, Exception) as e:
            logging.error("Connection to endpoint failed %s\n" % e)
            return response

        if response.status_code != requests.codes.ok:
            logging.error("sending data to endpoint failed with status code %s due to %s ", response.status_code,
                          response.text)
        logging.debug("Success in sending the event to Endpoint")
        return response
