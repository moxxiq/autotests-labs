from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from subprocess import Popen
import time
import unittest


class AppTest(unittest.TestCase):
    BACKEND_NAME = 'backend.py'
    START_URL = 'http://localhost:8000'
    LOGOUT_SIGNATURE = 'Log Out'
    header_pause = 2
    def setUp(self):
        self.backend_process = Popen(['python', self.BACKEND_NAME])
        self.driver = webdriver.Firefox()
        self.maxDiff = None

    def tearDown(self):
        # Despite of it's already in __exit__, memory won't free ¯\_(ツ)_/¯ idk
        self.driver.quit()
        self.backend_process.kill()
        self.backend_process.wait()

    def _log_in(self, driver, email, password):
        elem = driver.find_element(By.NAME, 'email')
        elem.clear()
        elem.send_keys(email)

        elem = driver.find_element(By.NAME, 'password')
        elem.clear()
        elem.send_keys(password)
        driver.find_element(By.XPATH, '//button[.="Log In"]').click()

    def _create_user(self, driver, name, email, password):
        name_field = driver.find_element(By.NAME, 'display_name')
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')

        # unary clearing doesn't work in multiple sessions
        name_field.send_keys()
        name_field.clear()
        name_field.send_keys(name)
        email_field.send_keys()
        email_field.clear()
        email_field.send_keys(email)
        password_field.send_keys()
        password_field.clear()
        password_field.send_keys(password)

        driver.find_element(By.XPATH, '//button[.="Sign Up"]').click()
        btn = driver.find_element(By.XPATH, '//button[.="Log Out"]')
        btn.click()

    def _post_comment(self, driver, numbers):
        # driver.find_element(By.XPATH, '//button[.="New comment"]').click()
        for i, n in enumerate(numbers):
            elem = driver.find_element(By.CSS_SELECTOR, f"input:nth-child({i + 1})")
            elem.clear()
            elem.send_keys(str(n))
        solve = driver.find_element(By.XPATH, '//button[.="Обчислити"]')
        solve.click()

    def _check_answer(self, driver, answer):
        elem_answer = driver.find_element(By.CSS_SELECTOR, "h3")
        answer_in_elem = elem_answer.text[11:]
        self.assertEqual(answer_in_elem, answer, "Answer isn't correct")

    def _check_last_comment(self, driver, comment, author):
        xp = f'//div[@id="comments"]/ul/li[last()][span="{comment}"]'\
            f'[a="{author}"][span/button="Remove"]'
        self.assertTrue(
            driver.find_element(By.XPATH, xp),
            'New comment is not correct')

    def test_1_anonymous(self):
        """
        1. Перевіряє, що анонімний користувач бачить на сторінці
        """
        with self.driver as driver:
            driver.get(self.START_URL)
            elems = driver.find_elements(
                By.XPATH, '//h1[.="Курсова робота"]')
            self.assertTrue(elems, 'Header is absent')

            elems = driver.find_elements(
                By.XPATH, '//h2[text()!=""]')
            self.assertTrue(elems, 'Condition body is empty')

            comments = (
                ('Input: [2, 4, 16, 256] Answer: 128.2692480682724', 'Linus T.'),
                ('Input: [1, -1, 4, -4] Answer: 2.9154759474226504', 'Iryna K.'),
            )

            for comment, elem in zip(
                comments,
                driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li')
            ):
                comment_text = elem.find_element(By.TAG_NAME, 'span').text
                author = elem.find_element(By.TAG_NAME, 'a').text
                self.assertEqual(comment, (comment_text, author),
                                 'Answers does not match')

            elems = driver.find_elements(By.XPATH, '//button[.="Sign Up"]')
            self.assertTrue(elems, 'Sign up button is missing')

            elems = driver.find_elements(By.XPATH, '//button[.="Log In"]')
            self.assertTrue(elems, 'Log In button is missing')
            # Display Name
            elems = driver.find_elements(
                By.XPATH, '//input[@name="display_name"]')
            self.assertTrue(
                elems, 'There is no field for entering a Display name')
            elems = driver.find_elements(
                By.XPATH, '//div[@id="signup-section"]/div/label[1]/b')
            self.assertTrue(
                elems, 'There is no label for a Display name')
            # Email
            elems = driver.find_elements(
                By.XPATH, '//input[@name="email"]')
            self.assertTrue(
                elems, 'There is no field for entering an Email')
            elems = driver.find_elements(
                By.XPATH, '//div[@id="signup-section"]/div/label[2]/b')
            self.assertTrue(
                elems, 'There is no label for an Email')
            # Password
            elems = driver.find_elements(
                By.XPATH, '//input[@name="password"]')
            self.assertTrue(
                elems, 'There is no field for entering a Password')
            elems = driver.find_elements(
                By.XPATH, '//div[@id="signup-section"]/div/label[3]/b')
            self.assertTrue(
                elems, 'There is no label for a Password')

    def test_2_signup(self):
        """
        2. Перевіряє, що новий користувач може зареєструватись
        """
        display_name = 'Carol C.'
        email = 'carol@gmail.com'
        password = 'ccc'

        with self.driver as driver:
            driver.get(self.START_URL)
            # signing up
            driver.find_element(
                By.NAME, 'display_name').send_keys(display_name)
            driver.find_element(By.NAME, 'email').send_keys(email)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.XPATH, "//div[@id='signup-section']/div/button").click()
            # Name check
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(
                raw_text[:-len(self.LOGOUT_SIGNATURE)-1], display_name)
            # Log out usage check
            btn = driver.find_element(By.XPATH, '//button[.="Log Out"]')
            # b
            btn.click()
            elems = driver.find_elements(By.XPATH, '//button[.="Log In"]')
            self.assertTrue(elems, 'User did not log out')
            # c
            other_display_name = 'Borya B.'
            elem = driver.find_element(By.NAME, 'display_name')
            elem.clear()
            elem.send_keys(other_display_name)

            elem = driver.find_element(By.NAME, 'email')
            elem.clear()
            elem.send_keys(email)

            elem = driver.find_element(By.NAME, 'password')
            elem.clear()
            elem.send_keys(password)

            driver.find_element(By.XPATH, '//button[.="Sign Up"]').click()

            elems = driver.find_elements(By.XPATH, '//button[.="Log Out"]')
            self.assertFalse(
                elems, 'User actually logged in with non unique email')

    def test_3_log_in(self):
        """
        3. Перевіряє, що зареєстрований користувач входить до свого облікового запису
        """
        email, password = 'torvalds@osdl.org', 'kernel'

        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self.assertTrue(driver.find_elements(
                By.XPATH, '//button[.="Log Out"]'))
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(
                raw_text[:-len(self.LOGOUT_SIGNATURE)-1], 'Linus T.')
            driver.find_element(By.XPATH, '//button[.="Log Out"]').click()

            self._log_in(driver, email, 'wrong-password')
            elems = driver.find_elements(By.XPATH, '//button[.="Log Out"]')
            self.assertFalse(
                elems, 'User actually logged in with wrong password')

            self._log_in(driver, 'wrong-email', password)
            elems = driver.find_elements(By.XPATH, '//button[.="Log Out"]')
            self.assertFalse(
                elems, 'User actually logged in with wrong email')

    def test_4_editor(self):
        """
        4. Перевіряє, що на сторінці є ввід завдань та кнопка Обчислити
        """
        email, password = 'torvalds@osdl.org', 'kernel'
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            elem = driver.find_element(By.XPATH, "//div[@id='values']/input")
            self.assertTrue(elem, 'Input values is absent')
            elem = driver.find_element(By.XPATH, '//button[.="Обчислити"]')
            self.assertTrue(elem, 'New comment button is missing')

    def test_5_comment(self):
        """
        5. Перевіряє, що користувач, може виконати завдання
        """
        name = 'Linus T.'
        email, password = 'torvalds@osdl.org', 'kernel'
        numbers = [3, 13, 33, 87]
        my_comment = "Input: [3, 13, 33, 87] Answer: 47.0"
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            # a
            self._post_comment(driver, numbers)
            self._check_answer(driver, "47")
            self._check_last_comment(driver, my_comment, name)
            # bad input
            self._post_comment(driver, [99, 'numbers', '', ''])
            self._check_answer(driver, "")

    def test_6_comment(self):
        """
        6. Перевіряє, що користувач, може ввести ще один коментар
        """
        name = 'Linus T.'
        email, password = 'torvalds@osdl.org', 'kernel'
        numbers_1 = (3, 13, 33, 87)
        numbers_2 = (-16, 16, -16, 16)
        comment_numbers = (numbers_1, numbers_2)
        comments = (
            "Input: [3, 13, 33, 87] Answer: 47.0",
            "Input: [-16, 16, -16, 16] Answer: 16.0",
        )
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            for numbers in comment_numbers:
                self._post_comment(driver, numbers)
            for comment, elem in zip(
                comments,
                driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li[position() > (last() - 2)]')
            ):
                comment_text = elem.find_element(By.TAG_NAME, 'span').text
                author = elem.find_element(By.TAG_NAME, 'a').text
                self.assertEqual((comment, name), (comment_text, author),
                                 'Comment does not match')

    def test_7_remove(self):
        """
        7. Перевіряє, що користувач може видалити створений ним коментар
        """
        name = 'Mary Jane'
        email, password = 'maryjane420@hh.org', 'canintoabyss'
        with self.driver as driver:
            driver.get(self.START_URL)
            self._create_user(driver, name, email, password)
            self._log_in(driver, email, password)
            comments_before = driver.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li/span[1]')
            self._post_comment(driver, [11, 13, 15])
            time.sleep(0.5)
            driver.find_element(By.XPATH, '//div[@id="comments"]/ul/li[last()]/span/button[.="Remove"]').click()
            time.sleep(0.5)
            comments_after = driver.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li/span[1]')
            c1 = list(map(lambda x: x.text, comments_before))
            c2 = list(map(lambda x: x.text, comments_after))

            self.assertEqual(c1, c2, "Коментарі 'до' і 'після' відрізняються")

    def test_8_multiplayer(self):
        """
        Перевіряє, що можуть бути активними два різних користувача
        """
        user_1 = ('User 1', 'u1@gmail.com', 'userone')
        user_2 = ('User 2', 'u2@gmail.com', 'usertwo')
        # create user 1, 2
        with webdriver.Firefox() as driver:
            driver.get(self.START_URL)
            self._create_user(driver, *user_1)
            self._create_user(driver, *user_2)

        with webdriver.Firefox() as driver_1, webdriver.Firefox() as driver_2:
            driver_1.get(self.START_URL)
            driver_2.get(self.START_URL)
            # a
            self._log_in(driver_1, *user_1[1:])
            self._post_comment(driver_1, [1, 2, 3])
            # b
            self._log_in(driver_2, *user_2[1:])
            self._post_comment(driver_2, [11, 22, 33])
            # add and remove
            self._post_comment(driver_1, [1, 2, 3])
            driver_1.find_element(By.XPATH, '//div[@id="comments"]/ul/li[last()]/span/button[.="Remove"]').click()

            comments_user_2 = driver_2.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li/span[1]')

            comments_user_1 = driver_1.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li/span[1]')
            c1 = list(map(lambda x: x.text, comments_user_1))
            c2 = list(map(lambda x: x.text, comments_user_2))
            self.assertEqual(c1, c2, "Коментарі в двох користувачів відображаються по-різному")
        with webdriver.Firefox() as driver:
            driver.get(self.START_URL)
            comments_after = driver.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li/span')
            c = list(map(lambda x: x.text, comments_after))
        self.assertEqual(c1, c)


if __name__ == '__main__':
    unittest.main()
