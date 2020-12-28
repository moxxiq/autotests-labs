from subprocess import Popen
import unittest
import requests
import pprint


class AppTest(unittest.TestCase):
    BACKEND_NAME = 'backend.py'
    START_URL = 'http://localhost:8000'
    LOGOUT_SIGNATURE = 'Log Out'

    TEST_USERS = (
        ('Linus T.', 'torvalds@osdl.org', 'kernel'),
        ('Iryna K.', 'kostushkoia5@gmail.com', 'numericalerror'),
    )

    def setUp(self):
        self.backend_process = Popen(['python', self.BACKEND_NAME])

    def tearDown(self):
        # Despite of it's already in __exit__, memory won't free ¯\_(ツ)_/¯ idk
        self.backend_process.kill()
        self.backend_process.wait()

    def test_login(self):
        test_user_1 = self.TEST_USERS[0]
        input_data = {'email': test_user_1[1], 'password': test_user_1[2]}

        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertTrue(response.status_code == 200)

        result = response.json()
        self.assertEqual(result['display_name'], test_user_1[0])
        self.assertIn('token', result)
        self.assertIn('user_id', result)

        input_data = {'email': test_user_1[1], 'password': 'incorrect password'}
        r = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertEqual(r.status_code, 403)

        input_data = {'email': 'incorrect email', 'password': test_user_1[2]}
        r = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertEqual(r.status_code, 403)

    def test_unauthorized_comment(self):
        # Let's just assume we know that test Bob's user id is 2.
        required_cookies = {'jwt': 'definitely incorrect security token'}
        data = {'user_id': 2,
                "numbers": [3434, 4343],
                "token": "asdfasdfasdf"}
        r = requests.post(self.START_URL + '/api/v1/task',
                          json=data, cookies=required_cookies)
        self.assertEqual(
            r.status_code, 401, 'Unauthorized request to add comment has actually succeeded')


if __name__ == '__main__':
    unittest.main()
