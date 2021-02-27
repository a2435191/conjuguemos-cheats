import requests
import logging
import time
import json

class ConjuguemosInterface():
    def __init__(self):
        self.s = requests.Session()

    def authenticate(self, username, password, additional_headers = {}, additional_payload = {}):
        """
        Authenticate so that `self.s` gets the required cookies to save scores
        :param str username: the target user's username
        :param str password: the target user's password
        :param dict additional_headers: additional headers to be sent with the request
        :param dict additional_payload: additional payload to be sent with the request
        :rtype: None
        """

        logging.info('Beginning authentication step.')
        
        headers = {}
        headers.update(additional_headers)

        payload = {
            'identity' : username, 
            'password' : password
        }
        payload.update(additional_payload)

        response = self.s.post('https://conjuguemos.com/auth/login', headers=headers, data=payload)
        response.raise_for_status()

        logging.info('Authentication step complete.')
    
    def save_score(self, activity_id, correct, attempts, time_taken=300, mode='homework', attempts_data=[["",1,"0","0","0","0","0"]], additional_headers={}, additional_payload={}):
        """
        Make a request to the conjuguemos servers to add a score.
        :param int activity_id: target activity's id, usually found near the end of the url
        :param int correct: number of correct answers (score numerator)
        :param int attempts: total number of submitted answers (score denominator)
        :param int time_taken: time taken for the exercise in seconds
        :param str mode: mode for request; change from default at own risk. TODO: implement alternatives
        :param list attempts_data: list of lists; each sub-list has seven parameters: 
            the first is the user input for a question,
            the second is 1 or 0 and indicates if the question was answered correctly,
            the function of the final five items is unknown, but they are all numeric strings.
        :param dict additional_headers: additional headers to be sent with the request
        :param dict additional_payload: additional payload to be sent with the request
        :rtype: None
        """
        logging.info('Beginning score addition step.')

        if mode != 'homework':
            logging.warning('Other modes are untested. Proceed with caution.')
        activity_start = int(time.time())
        activity_end = activity_start + time_taken

        payload = {
            'activity_id': activity_id,
            'mode': mode,
            'activity_start': activity_start,
            'activity_end': activity_end,
            'data[attemps]': json.dumps(attempts_data),
            'data[total_attemps]': attempts,
            'data[valid_attemps]': correct
        }
        payload.update(additional_payload)

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        headers.update(additional_headers)

        response = self.s.post('https://conjuguemos.com/verb/submit', data=payload, headers=headers)
        response.raise_for_status()

        logging.info('Score added.')
