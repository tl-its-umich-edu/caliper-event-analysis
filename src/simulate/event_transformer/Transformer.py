import logging
import utils
import random
import json


class Transformer:
    USER_STR = "https://mcommunity.umich.edu/#profile:"

    def __init__(self, eventData, config_data):
        self.eventData = eventData
        self.envelope = eventData
        self.event = self.eventData['data'][0]
        self.config_data = config_data

    def change_user_in_event(self):
        try:
            sample_users = self.config_data[utils.PROPS_USERS]
        except KeyError:
            logging.error('configuration yaml is missing the \"users\" key')
            return

        if sample_users is None:
            logging.error('No Users information added to the configuration yml file')
            return
        user = random.choice(sample_users)
        user_id = self.USER_STR + user[utils.PROPS_USER_ID]
        user_sis_id = user[utils.PROPS_USER_SIS_ID]
        user_canvas_id = user[utils.PROPS_USER_CANVAS_ID]
        self.event['actor'] = user_id
        self.event['session']['user'] = user_id
        self.event['membership']['member'] = user_id
        # federated user info
        fed_session = self.event['federatedSession']
        fed_msg_params = fed_session['messageParameters']
        fed_session['user'] = user_id
        fed_msg_params['custom_canvas_user_id'] = user_canvas_id
        fed_msg_params['lis_person_sourcedid'] = user_sis_id
        return user

    def change_course_info(self, user):
        action = self.event['action']
        try:
            sample_courses = self.config_data[utils.PROPS_COURSES]
        except KeyError:
            logging.error('configuration yaml is missing the \"courses\" key')
            return

        if sample_courses is None:
            logging.error('No courses information added to the configuration yml file')
            return

        a_course_info = random.choice(sample_courses)
        # targeted to Media events
        if action != 'LoggedIn':
            logging.debug('Action=%s', action)
            object = self.event['object']
            target = self.event['target']
            video_player = random.choice(a_course_info[utils.PROPS_VIDEO_PLAYER])
            video_id = video_player[utils.PROPS_USER_ID]
            object['id'] = video_id
            object['name'] = video_player[utils.PROPS_PLAYER_NAME]
            object['isPartOf']['id'] = a_course_info[utils.PROPS_COURSE_SITE]
            object['isPartOf']['name'] = a_course_info[utils.PROPS_COURSE_NAME]
            target['id'] = video_id + '#type=MediaLocation'
            target['isPartOf'] = video_id
        # group and membership is part of all elements

        # group
        group = self.event['group']
        group_id = a_course_info['course_site'] + '#' + group['type']
        group['id'] = group_id
        group['courseNumber'] = a_course_info['course_name']
        # membership
        membership = self.event['membership']
        membership['id'] = a_course_info['course_site'] + '#' + membership['type'] + '&member=' + user['id']
        membership['organization'] = group_id
        # federated course info
        fed_session = self.event['federatedSession']
        fed_msg_params = fed_session['messageParameters']
        fed_msg_params['custom_canvas_course_id'] = a_course_info[utils.PROPS_COURSE_CANVAS_ID]
        fed_msg_params['lis_course_offering_sourcedid'] = a_course_info[utils.PROPS_COURSE_SIS_ID]
        fed_session['id'] = 'urn:instructure:canvas:umich:session:' + utils.get_random_alpha_numeric_string(38)

    def change_session_info(self):
        session = self.event['session']
        session_id = utils.get_random_alpha_numeric_string(19)
        session['id'] = 'urn:umich:engin:leccap:session:' + session_id

    def change_duration_and_current_time(self):
        action = self.event['action']
        if action != 'LoggedIn':
            duration = utils.random_number_with_n_digits(4)
            self.event['object']['duration'] = 'PT' + str(duration) + '.000S'
            if action != 'Started':
                current_time = utils.get_random_floating_point_number(duration)
                self.event['target']['currentTime'] = 'PT' + str(current_time) + 'S'

    def transformer(self):
        self.event['eventTime'] = utils.get_current_date_time_iso8601_format()
        self.envelope['sendTime'] = utils.get_current_date_time_iso8601_format()
        self.event['id'] = utils.get_uuid()
        user = self.change_user_in_event()
        self.change_course_info(user)
        self.change_session_info()
        self.change_duration_and_current_time()

        logging.debug(json.dumps(self.eventData, indent=4))
        logging.debug("-------------------------------------------")
        return self.eventData
