import unittest
import utils


class TestMovingAverage(unittest.TestCase):

    def test_simple(self):
        data = [1, 2, 3]
        correct = [0.0, 1.5, 2.5]
        result = list(utils.moving_average(data, 2))
        self.assertListEqual(result, correct)

    def test_zero_len(self):
        data = []
        correct = []
        result = list(utils.moving_average(data, 0))
        self.assertListEqual(result, correct)

    def test_one_element(self):
        data = [5]
        correct = [5.0]
        result = list(utils.moving_average(data, 1))
        self.assertListEqual(result, correct)

    def test_eq_len(self):
        data = [1, 2, 3]
        correct = [0.0, 0.0, 2.0]
        result = list(utils.moving_average(data, 3))
        self.assertListEqual(result, correct)

    def test_bigger_len(self):
        data = [1, 2, 3]
        with self.assertRaises(ValueError):
            result = list(utils.moving_average(data, 4))  # noqa


if __name__ == "__main__":
    unittest.main()
