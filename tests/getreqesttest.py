import unittest

import getrequest
import properties

USERNAME = 'bob'
OTHER_USERNAME = 'joe'
PASSWORD = 'XXXX'
OTHER_PASSWORD = 'YYYY'
PROTOCOL = 'https://'
URL = 'members.easynews.com/dl/iad/447/418bb2aae1121bed3349bc29a57d2a6301814fa671f16.jpg/00-hans_zimmer_and_james_newton_howard-the_dark_knight-ost-cd-flac-2008-proof.jpg?sid=7dfcd27e1b6b7e880d77a8449309e18d09452114:0&sig=MTY5MTk1NDkyNC08YXV0b3Jhci0yYWI0YzVkNGE0MzM0ZjA3OWU0ZTM0ZjY2OTAzMGIyYkBuZ1Bvc3QtOTE0NTdlMTA+'
SESSION_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
OTHER_SESSION_ID = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

class GetRequestTestCase(unittest.TestCase):
    def init_credentials(self, username=USERNAME, password=PASSWORD):
        properties.set_property('username', username)
        properties.set_property('password', password)

    def test_auth_url_without_session_id(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL
        self.assertEqual(desired, actual)

    def test_auth_url_with_none_session_id(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL, None)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL
        self.assertEqual(desired, actual)

    def test_auth_url_with_session_id(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL, SESSION_ID)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL + '|' + getrequest.session_id_cookie + '=' + SESSION_ID
        self.assertEqual(desired, actual)

    def test_auth_url_second_time(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL)
        actual = getrequest.url_auth(actual)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL
        self.assertEqual(desired, actual)

    def test_auth_url_username_password_changed(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL
        self.assertEqual(desired, actual)

        self.init_credentials(OTHER_USERNAME, OTHER_PASSWORD)
        actual = getrequest.url_auth(actual)
        desired = PROTOCOL + OTHER_USERNAME + ':' + OTHER_PASSWORD + '@' + URL
        self.assertEqual(desired, actual)

    def test_auth_url_with_session_id_changed(self):
        self.init_credentials()
        actual = getrequest.url_auth(PROTOCOL + URL, SESSION_ID)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL + '|' + getrequest.session_id_cookie + '=' + SESSION_ID
        self.assertEqual(desired, actual)

        actual = getrequest.url_auth(actual, OTHER_SESSION_ID)
        desired = PROTOCOL + USERNAME + ':' + PASSWORD + '@' + URL + '|' + getrequest.session_id_cookie + '=' + OTHER_SESSION_ID
        self.assertEqual(desired, actual)

if __name__ == '__main__':
    unittest.main()
