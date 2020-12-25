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

    def setUp(self):
        self.backend_process = Popen(['python', self.BACKEND_NAME])
        self.driver = webdriver.Firefox()

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

    def _post_comment(self, driver, text_comment):
        driver.find_element(By.CLASS_NAME, 'ql-editor').clear()
        driver.find_element(By.CLASS_NAME, 'ql-editor').send_keys(text_comment)
        driver.find_element(By.XPATH, '//button[.="New comment"]').click()

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
            # a
            elems = driver.find_elements(
                By.XPATH, '//h1[.="Is this a good way to process input?"]')
            self.assertTrue(elems, 'Question header is absent')

            # b
            elems = driver.find_elements(
                By.XPATH, '//div[@id="question"]/pre[text()!=""]')
            self.assertTrue(elems, 'Question body is empty')

            # c
            comments = (
                ('Test comment 1', 'Alice A.'),
                ('Test comment 2', 'Bob B.'),
            )

            for comment, elem in zip(
                comments,
                driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li')
            ):
                comment_text = elem.find_element(By.TAG_NAME, 'span').text
                author = elem.find_element(By.TAG_NAME, 'a').text
                self.assertEqual(comment, (comment_text, author),
                                 'Comment does not match')

            # d
            elems = driver.find_elements(By.XPATH, '//button[.="Sign Up"]')
            self.assertTrue(elems, 'Sign up button is missing')

            elems = driver.find_elements(By.XPATH, '//button[.="Log In"]')
            self.assertTrue(elems, 'Log In button is missing')

            # e
            # Display Name
            elems = driver.find_elements(
                By.XPATH, '//div[input[@name="display_name"]]')
            self.assertTrue(
                elems, 'There is no field for entering a Display name')
            elems = driver.find_elements(
                By.XPATH, '//div[label[@for="name"]/b]')
            self.assertTrue(
                elems, 'There is no label for a Display name')
            # Email
            elems = driver.find_elements(
                By.XPATH, '//div[input[@name="email"]]')
            self.assertTrue(
                elems, 'There is no field for entering an Email')
            elems = driver.find_elements(
                By.XPATH, '//div[label[@for="email"]/b]')
            self.assertTrue(
                elems, 'There is no label for an Email')
            # Password
            elems = driver.find_elements(
                By.XPATH, '//div[input[@name="password"]]')
            self.assertTrue(
                elems, 'There is no field for entering a Password')
            elems = driver.find_elements(
                By.XPATH, '//div[label[@for="psw"]/b]')
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
            # a
            # signing up
            driver.find_element(
                By.NAME, 'display_name').send_keys(display_name)
            driver.find_element(By.NAME, 'email').send_keys(email)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.XPATH, '//button[.="Sign Up"]').click()
            # Name check
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(
                raw_text[:-len(self.LOGOUT_SIGNATURE)], display_name)
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
        email, password = 'alice_2002@gmail.com', 'aaa'

        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self.assertTrue(driver.find_elements(
                By.XPATH, '//button[.="Log Out"]'))
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(
                raw_text[:-len(self.LOGOUT_SIGNATURE)], 'Alice A.')
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
        4. Перевіряє, що на сторінці є Редактор та кнопка New comment
        """
        email, password = 'alice_2002@gmail.com', 'aaa'
        my_script = """
        var elem = document.getElementById('editor-section');
        elem.style.borderColor = "red";
        elem.style.borderStyle = "solid";
        """
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            elem = driver.find_element(By.ID, 'editor-section')
            self.assertTrue(elem, 'Editor section is not present')
            elem = driver.find_element(By.XPATH, '//button[.="New comment"]')
            self.assertTrue(elem, 'New comment button is missing')

            driver.execute_script(my_script)
            driver.save_screenshot('comments_screenshot.png')

    def test_5_comment(self):
        """
        5. Перевіряє, що користувач, може ввести новий коментар
        """
        def click_style(style_name):
            driver.find_element(By.CLASS_NAME, 'ql-' + style_name).click()

        name = "Alice A."
        email, password = 'alice_2002@gmail.com', 'aaa'
        my_comment = 'Comment from Alice'
        expected_formatted_comment_html = '<span><strong>Comment</strong> '\
            '<em>from <s>Alice</s></em> <u>Dmytro</u></span>'

        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            # a
            self._post_comment(driver, my_comment)
            self._check_last_comment(driver, my_comment, name)
            # b
            text_field = driver.find_element(By.CLASS_NAME, 'ql-editor')
            text_field.clear()
            click_style('bold')
            text_field.send_keys('Comment')
            click_style('bold')
            text_field.send_keys(' ')
            click_style('italic')
            text_field.send_keys('from ')
            click_style('strike')
            text_field.send_keys('Alice')
            click_style('strike')
            click_style('italic')
            text_field.send_keys(' ')
            click_style('underline')
            text_field.send_keys('Dmytro')
            click_style('underline')
            driver.find_element(By.XPATH, '//button[.="New comment"]').click()

            elem = driver.find_element(
                By.XPATH, '//div[@id="comments"]/ul/li[last()]/span')
            extracted_html = elem.get_attribute('outerHTML')
            self.assertEqual(extracted_html, expected_formatted_comment_html)
            # c
            self._check_last_comment(driver, "Comment from Alice Dmytro", name)

    def test_6_comment(self):
        """
        6. Перевіряє, що користувач, може ввести ще один коментар
        """
        name = "Alice A."
        email, password = 'alice_2002@gmail.com', 'aaa'
        comments = ('Previous Alice comment', 'Current Alice comment')
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            # a
            for comment in comments:
                self._post_comment(driver, comment)
                self._check_last_comment(driver, comment, name)
            # b
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
        email, password = 'alice_2002@gmail.com', 'aaa'
        comment = 'Alice comment'
        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            comments_before = driver.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li')
            self._post_comment(driver, comment)
            driver.find_element(By.XPATH, '//div[@id="comments"]/ul/li[last()]/span/button[.="Remove"]').click()
            comments_after = driver.find_elements(
                By.XPATH,
                '//div[@id="comments"]/ul/li')
            self.assertEqual(comments_before, comments_after)

    def test_8_multiplayer(self):
        pass


if __name__ == '__main__':
    unittest.main()
