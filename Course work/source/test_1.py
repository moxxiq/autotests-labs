import unittest
from backend import root_mean_square


class TestTask1(unittest.TestCase):
    """Unit test task_1"""

    def test_valid_input(self):
        inp = [3, 13, 33, 87]
        self.assertAlmostEqual(root_mean_square(inp), 47)

    def test_zeros(self):
        inp = [0, 0, 0]
        self.assertAlmostEqual(root_mean_square(inp), 0)

    def test_negative(self):
        inp = [-99, -99, -1]
        self.assertAlmostEqual(root_mean_square(inp), 80.83522334)

    def test_real(self):
        inp = [0.3331, 5.032, -8989]
        self.assertAlmostEqual(root_mean_square(inp), 5189.80238647)

    def test_no_input(self):
        inp = []
        self.assertAlmostEqual(root_mean_square(inp), None)

    def test_type_error(self):
        inp = ['1', 90, 4]
        self.assertRaises(TypeError, root_mean_square, inp)


if __name__ == "__main__":
    unittest.main()
