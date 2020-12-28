from subprocess import Popen, PIPE
import unittest
import requests
import pprint
from time import sleep


class AppTest(unittest.TestCase):
    BACKEND_NAME = 'backend.py'
    START_URL = 'http://localhost:8000'
    LOGOUT_SIGNATURE = 'Log Out'

    Linus = ('Linus T.', 'torvalds@osdl.org', 'kernel')
    Iryna = ('Iryna K.', 'kostushkoia5@gmail.com', 'numericalerror')

    def setUp(self):
        self.backend_process = Popen(
            ['python', self.BACKEND_NAME],)
        sleep(2)

    def tearDown(self):
        # Despite of it's already in __exit__, memory won't free ¯\_(ツ)_/¯ idk
        self.backend_process.kill()
        self.backend_process.wait()

    def test_login(self):
        """
        Вхід зареєстрованого користувача
        """
        input_data = {'email': self.Linus[1], 'password': self.Linus[2]}

        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertTrue(response.status_code == 200)

        result = response.json()
        self.assertEqual(result['display_name'], self.Linus[0])
        self.assertIn('token', result)
        self.assertIn('user_id', result)

    def test_wrong_pass(self):
        """
        Вхід з невірним паролем
        """
        input_data = {'email': self.Linus[1], 'password': 'incorrect password'}
        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertEqual(response.status_code, 403)

    def test_wrong_login(self):
        """
        Вхід з невірним логіном
        """
        input_data = {'email': 'incorrect email', 'password': self.Linus[1]}
        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_comment(self):
        """
        Створення коментаря в обхід входу
        """
        # Let's just assume we know that test Bob's user id is 2.
        required_cookies = {'jwt': 'definitely incorrect security token'}
        data = {'user_id': 2,
                "numbers": [3434, 4343]}
        response = requests.post(
            self.START_URL + '/api/v1/task',
            json=data, cookies=required_cookies)
        self.assertEqual(
            response.status_code, 401, 'Unauthorized request to add comment has actually succeeded')

    def test_logout(self):
        """
        Вихід з облікового запису
        """
        # login
        input_data = {'email': self.Linus[1], 'password': self.Linus[2]}
        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        result = response.json()
        jwt = result['token']
        # logout
        data = {'id': result['user_id'], }
        required_cookies = {'jwt': jwt}
        r = requests.post(self.START_URL + '/api/v1/user/logout',
                          json=data, cookies=required_cookies)
        self.assertEqual(
            r.status_code, 200, "User can't log out")

    def test_authorized_comment(self):
        """
        Вирішення задачі з вхідними данними і створення коментаря
        """
        # login
        input_data = {'email': self.Linus[1], 'password': self.Linus[2]}
        response = requests.post(
            self.START_URL + '/api/v1/user/login', json=input_data)
        result = response.json()
        jwt = result['token']
        required_cookies = {'jwt': jwt}
        data = {'user_id': result['user_id'],
                "numbers": [3, 13, 33, 87]}
        r = requests.post(self.START_URL + '/api/v1/task',
                          json=data, cookies=required_cookies)
        expected = {"comments": [
            {
                "id": 1,
                "text": "Input: [2, 4, 16, 256] Answer: 128.2692480682724",
                "user_id": 1,
                "display_name": "Linus T."
            },
            {
                "id": 2,
                "text": "Input: [1, -1, 4, -4] Answer: 2.9154759474226504",
                "user_id": 2,
                "display_name": "Iryna K."
            },
            {
                "id": 3,
                "text": "Input: [3, 13, 33, 87] Answer: 47.0",
                "user_id": 1,
                "display_name": "Linus T."
            }
        ],
            "answer": 47.0
        }
        self.assertEqual(
            r.json(), expected, "Can't post comments")

    def test_singin(self):
        """
        Реєстрація нового користувача
        """
        input_data = {"display_name": "Dmytro",
                      "password": "dima",
                      "email": "dimanavsisto@gmail.com"}
        response = requests.post(
            self.START_URL + '/api/v1/user/signup', json=input_data)
        result = response.json()
        expected = {
            "token": "aef6967d-f444-45ec-a624-47b6ec7c2c12",
            "user_id": 3,
            "display_name": "Dmytro"}
        self.assertEqual(
            result["display_name"], expected["display_name"], "User can't signin")

    def test_singin_existing(self):
        """
        Реєстрація існуючого користувача
        """
        input_data = {
            "display_name": self.Linus[0],
            "password": self.Linus[2],
            "email": self.Linus[1]}
        response = requests.post(
            self.START_URL + '/api/v1/user/signup', json=input_data)
        self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main(warnings="ignore")
