import logging
import utils
import random
import json


class Transformer:
    CONST_USER_STR = "https://mcommunity.umich.edu/#profile:"

    def __init__(self, eventData, config_data):
        self.eventData = eventData
        self.envelope = eventData
        self.event = self.eventData['data'][0]
        self.config_data = config_data

    def change_user_in_event(self):
        try:
            sample_users = self.config_data['users']
        except KeyError:
            logging.error("configuration yaml is missing the \"users\" key")
            return

        if sample_users is None:
            logging.error("No Users information added to the configuration yml file")
            return
        user_id = self.CONST_USER_STR + random.choice(sample_users)['id']
        self.event['actor']['id'] = user_id
        self.event['session']['user']['id'] = user_id
        self.event['membership']['member'] = user_id

    def change_course_info(self):
        action = self.event['action']
        try:
            sample_courses = self.config_data['courses']
        except KeyError:
            logging.error("configuration yaml is missing the \"courses\" key")
            return

        if sample_courses is None:
            logging.error("No courses information added to the configuration yml file")
            return

        a_course_info = random.choice(sample_courses)
        # targeted to Media events
        if action != 'LoggedIn':
            logging.debug("Action=%s", action)
            object = self.event['object']
            target = self.event['target']
            video_player = random.choice(a_course_info['video_player'])
            object['id'] = video_player
            object['isPartOf']['id'] = a_course_info['course_site']
            object['isPartOf']['name'] = a_course_info['course_name']
            target['id'] = video_player
            target['isPartOf']['id'] = video_player
        # group and membership is part of all elements
        group = self.event['group']
        membership = self.event['membership']
        group_id = a_course_info['course_site'] + "#" + group['type']
        group['id'] = group_id
        group['courseNumber'] = a_course_info['course_name']
        membership['id'] = a_course_info['course_site'] + "#" + membership['type']
        membership['organization'] = group_id

    def change_session_info(self):
        session = self.event['session']
        session_id = utils.get_random_alpha_numeric_string(19)
        session['id'] = "urn:umich:engin:leccap:session:" + session_id
        session['name'] = "session-" + session_id

    def event_transformer(self):
        self.envelope['sendTime'] = utils.get_current_date_time_iso8601_format()

        self.event['eventTime'] = utils.get_current_date_time_iso8601_format()
        self.event['id'] = utils.get_uuid()
        self.change_user_in_event()
        self.change_course_info()
        self.change_session_info()
        logging.debug(json.dumps(self.eventData, indent=4))
        logging.debug("-------------------------------------------")
        return self.eventData
