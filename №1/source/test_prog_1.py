import prog_1
import unittest


class Prog_1Test(unittest.TestCase):

    def test_simple_equality(self):
        self.assertEqual(prog_1.closer((2.2, 3.3), (-3.3, -2.2)), [])

    def test_int_compatibility(self):
        self.assertEqual(prog_1.closer((22, 33), (-31, -24)), [(-31, -24)])

    def test_big_numbers(self):
        self.assertEqual(prog_1.closer(
            (1000000000000000000000.2, -90000000000000000000000.4), (1221221, 32312321)),
            [(1221221, 32312321)])

    def test_negative_test(self):
        self.assertEqual(prog_1.closer((-9.0, 9.0), (1.1, 1.1)), [(1.1, 1.1)])

    def test_bad_data(self):
        self.assertRaises(TypeError, prog_1.closer, (-9.0, 9.0), (1.1, 'o'))


if __name__ == '__main__':
    unittest.main()
