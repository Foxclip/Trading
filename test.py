import unittest
import utils
import simulation
import strategies


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


class TestSimulation(unittest.TestCase):

    def setUp(self):
        simulation.init()

    def test_ma(self):
        simulation.global_settings.precision = 5
        simulation.global_settings.amount = 100
        simulation.global_settings.step_output = False
        simulation.load_file("test/test_small.csv")
        template = {
            "balance": simulation.to_curr(100.0),
            "ignore_spread": False,
            "sl_range": 10,
            "tp_range": 10,
            "ma1": 5,
            "ma2": 10,
            "leverage": 500,
            "direction": simulation.Direction.REVERSE,
            "strategy": strategies.moving_averages,
            "name": "Untitled"
        }
        simulation.sim_list([template], plotting=[])
        balance = simulation.from_curr(simulation.simulations[0].balance)
        self.assertEqual(balance, 98.88)

    def test_macd(self):
        simulation.global_settings.precision = 5
        simulation.global_settings.amount = 200
        simulation.global_settings.step_output = False
        simulation.load_file("test/test_small.csv")
        template = {
            "balance": simulation.to_curr(100.0),
            "ignore_spread": False,
            "sl_range": 10,
            "tp_range": 10,
            "macd_s": 12,
            "macd_l": 26,
            "macd_t": 9,
            "leverage": 500,
            "direction": simulation.Direction.REVERSE,
            "strategy": strategies.macd,
            "name": "Untitled"
        }
        simulation.sim_list([template], plotting=[])
        balance = simulation.from_curr(simulation.simulations[0].balance)
        self.assertEqual(balance, 99.44)


if __name__ == "__main__":
    unittest.main(buffer=True)
