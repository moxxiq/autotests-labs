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
        # No need to add self.driver.quit() it's already in __exit__
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

    def test_1_anonymous(self):
        """
        Task 1
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
        Task 2
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

# Task 3 Log in for existing user - Alice A.

    def test_3_log_in(self):

        email, password = 'alice_2002@gmail.com', 'aaa'

        with self.driver as driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)
            
            self.assertTrue(driver.find_elements(
                By.XPATH, '//button[.="Log Out"]'))
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(
                raw_text[:-len(self.LOGOUT_SIGNATURE)], 'Alice A.')

            

# Task 4 Log in for existing user - Alice A.

    # def test_editor(self):

    #     email, password = 'alice_2002@gmail.com', 'aaa'
    #     my_script = """
    #     var elem = document.getElementById('editor-section');
    #     elem.style.borderColor = "red";
    #     elem.style.borderStyle = "solid";
    #     """

    #     with self.driver as driver:
    #         driver.get(self.START_URL)
    #         self._log_in(driver, email, password)

    #         elem = driver.find_element(By.ID, 'editor-section')
    #         self.assertTrue(elem, 'Editor section is not present')
    #         elem = driver.find_element(By.XPATH, '//button[.="New comment"]')
    #         self.assertTrue(elem, 'New comment button is missing')

    #         driver.execute_script(my_script)
    #         driver.save_screenshot('my_screen.png')


# Test 5. Check for an existing user, for example, - Alice A.
    # def test_comment(self):

    #     def click_style(style_name):
    #         driver.find_element(By.CLASS_NAME, 'ql-' + style_name).click()

    #     email, password = 'alice_2002@gmail.com', 'aaa'
    #     my_comment = 'Comment from Alice'
    #     expected_formatted_comment_html = '<span><strong>Comment</strong> from Alice</span>'

    #     with self.driver as driver:
    #         driver.get(self.START_URL)
    #         self._log_in(driver, email, password)

    #         self._post_comment(driver, my_comment)
    #         xp = '//div[@id="comments"]/ul/li[last()][span="{}"][a="Alice A."][span/button="Remove"]'.format(my_comment)
    #         self.assertTrue(driver.find_element(By.XPATH, xp),
    #                         'New comment is not correct')

    #         driver.find_element(By.CLASS_NAME, 'ql-editor').clear()
    #         elem = driver.find_element(By.CLASS_NAME, 'ql-editor')
    #         click_style('bold')
    #         elem.send_keys('Comment')
    #         click_style('bold')
    #         elem.send_keys(' from Alice')
    #         driver.find_element(By.XPATH, '//button[.="New comment"]').click()

    #         elem = driver.find_element(
    #             By.XPATH, '//div[@id="comments"]/ul/li[last()]/span')
    #         extracted_html = elem.get_attribute('outerHTML')
    #         self.assertEqual(extracted_html, expected_formatted_comment_html)


if __name__ == '__main__':
    unittest.main()
