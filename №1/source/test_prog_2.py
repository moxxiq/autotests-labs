import prog_2
import unittest


class Prog_2Test(unittest.TestCase):

    def test_straight_sum(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [1, -6, 0, 34, 434]
            ),
            462
        )

    def test_empty(self):
        self.assertEqual(
            prog_2.sum_min_max(
                []
            ),
            0
        )

    def test_one(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [41]
            ),
            41
        )

    def test_two(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [1, 2]
            ),
            3
        )

    def test_reverse_sum(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [1, 434, 0, 34, -6]
            ),
            462
        )

    def test_float_compatibility(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [1.32, -6.23, 0, 34, 434.001]
            ),
            461.77099999999996
        )

    def test_negative_test(self):
        self.assertEqual(
            prog_2.sum_min_max(
                [-794, -43, -8989, -11, -89]
            ),
            -9000
        )

    def test_multiple_minmax(self):
        self.assertIn(
            prog_2.sum_min_max(
                [-89, 1, 90, -89, 2, 90]
            ),
            [2, 5, 1, 3]
        )

    def test_nested_lst(self):
        self.assertRaises(TypeError, prog_2.sum_min_max, [12, [21, 32]])

    def test_bad_type_sum(self):
        self.assertRaises(TypeError, prog_2.sum_min_max, [1, 'o', 2])

    def test_bad_type_cmp(self):
        self.assertRaises(TypeError, prog_2.sum_min_max, [1, 2, 'o'])


if __name__ == '__main__':
    unittest.main()
