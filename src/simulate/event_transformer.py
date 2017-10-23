import datetime
import json
import logging
from json import JSONDecodeError


class Transformer:
    def __init__(self, event):
        self.event = event

    def get_current_date_time_iso8601_format(self):
        strftime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
        strftime = strftime[:-3] + 'Z'
        return strftime

    def event_transformer(self):
        try:
            json_event = json.loads(self.event)
        except JSONDecodeError as e:
            logging.error("Failed to Deserialize the caliper event %s ",e)
            return None
        data = json_event['data']
        data[0]['eventTime'] = self.get_current_date_time_iso8601_format()
        json_event['sendTime'] = self.get_current_date_time_iso8601_format()
        return json_event
