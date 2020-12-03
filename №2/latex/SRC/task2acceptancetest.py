import locale
from subprocess import Popen, PIPE, TimeoutExpired
import unittest


class TestTask1(unittest.TestCase):
    """Acceptance test task_1"""
    SCRIPT_NAME = "task_2.py"
    INPUT_SIGNATURE = "Введіть елементи масиву через пробіл\n"
    PROCESS_TIMEOUT = 5
    ENCODING = locale.getpreferredencoding()

    def run_subprocess(self, input_value):
        """Run subprocess for testing"""
        try:
            proc = Popen(["python", self.SCRIPT_NAME],
                         stdin=PIPE,
                         stdout=PIPE,
                         stderr=PIPE)
            out_value, err_value = proc.communicate(
                input_value.encode(self.ENCODING),
                timeout=self.PROCESS_TIMEOUT)
        except TimeoutExpired:
            proc.kill()
            out_value, err_value = proc.communicate()
        return out_value.decode(self.ENCODING), err_value.decode(self.ENCODING)

    def test_valid_input(self):
        input_data = (
            # plain
            ("Practice makes perfect", "perfect Practice makes"),
            # numbers
            ("1 2 3 4 5", "5 1 2 3 4"),
            # another language with '
            ("П'ятий човен на дно йшов", "йшов П'ятий човен на дно"),
            # just apostrophes
            ("'''''' ''''' '' '''", "''' '''''' ''''' ''"),
            # spaces
            ("         ", ""),
            # blank
            ("", ""),
            # plain sentence, comma
            ("here ar3e many wa``ys to sort them - by suits (diamonds, clubs, hearts, and spades) or by numbers",
             "numbers here ar3e many wa``ys to sort them - by suits (diamonds, clubs, hearts, and spades) or by"),
        )

        for input_str, expect_str in input_data:
            output_str, error_str = self.run_subprocess(input_str + '\n')
            actual_result = output_str.replace(self.INPUT_SIGNATURE, '').replace("\n", '')
            self.assertEqual(actual_result, expect_str)


if __name__ == "__main__":
    unittest.main()
