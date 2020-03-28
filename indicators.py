import simulation
import utils
import numpy as np
from numba import njit


def calc_ma(length, data=None):
    if data is None:
        data = simulation.global_data.price_data
    return utils.moving_average(data, length)


class Indicator:

    def __init__(self):
        self.data = []

    def calculate(self):
        raise NotImplementedError()


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length
        self.data = calc_ma(self.length)


class MACD(Indicator):

    def __init__(self, short, long, third):
        Indicator.__init__(self)
        self.short = short
        self.long = long
        self.third = third
        short_ma = calc_ma(short)
        long_ma = calc_ma(long)
        short_ma[:long - 1] = np.zeros(long - 1)
        diff = long_ma - short_ma
        self.data = calc_ma(third, diff)
        import matplotlib.pyplot as plt
        # plt.plot(short_ma[:30])
        # plt.plot(long_ma[:30])
        plt.plot(diff)
        plt.plot(self.data)
        # plt.plot(simulation.global_data.price_data)
        # plt.plot(calc_ma(short)[1000:1100])
        # plt.plot(calc_ma(long)[1000:1100])
        # plt.plot(calc_ma(calc_ma(long) - calc_ma(short))[1000:2000])
        plt.show()
        import sys
        sys.exit(0)


@njit
def detect_cross(lst1, lst2, offset):
    v1 = lst1[offset - 1]
    v2 = lst2[offset - 1]
    v1p = lst1[offset - 2]
    v2p = lst2[offset - 2]
    lst1_not_above_lst2 = v1 - v2 <= 0
    it_was_above_lst2 = v1p - v2p > 0
    lst1_not_below_lst2 = v1 - v2 >= 0
    it_was_below_lst2 = v1p - v2p < 0
    cross_above = lst1_not_above_lst2 and it_was_above_lst2
    cross_below = lst1_not_below_lst2 and it_was_below_lst2
    return cross_above, cross_below
