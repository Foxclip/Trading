import simulation
import utils
import numpy as np
from numba import njit
import matplotlib.pyplot as plt


indicators = None


def calc_ma(length, data=None):
    if data is None:
        data = simulation.global_data.price_data
    return utils.moving_average(data, length)


def get_ma(length):
    ma_name = f"ma{length}"
    if ma_name not in indicators:
        ma = MovingAverage(length)
        indicators[ma_name] = ma
        return ma
    else:
        return indicators[ma_name]


def get_macd(short, long, third):
    macd_name = f"macd_{short}_{long}_{third}"
    if macd_name not in indicators:
        macd = MACD(short, long, third)
        indicators[macd_name] = macd
        return macd
    else:
        return indicators[macd_name]


class Indicator:

    def __init__(self):
        self.data = []

    def plot(self):
        raise NotImplementedError()

    def requires_subplot(self):
        raise NotImplementedError()


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length
        self.data = calc_ma(self.length)

    def plot(self):
        cleared_data = self.data.copy()
        cleared_data = cleared_data[self.length - 1:]
        x_data = list(range(self.length - 1, len(self.data)))
        plt.plot(x_data, simulation.from_curr(cleared_data))

    def requires_subplot(self):
        return False


class MACD(Indicator):

    def __init__(self, short, long, third):
        Indicator.__init__(self)
        self.short = short
        self.long = long
        self.third = third
        short_ma = get_ma(short).data[:]
        long_ma = get_ma(long).data
        short_ma[:long - 1] = np.zeros(long - 1)
        diff = long_ma - short_ma
        self.data = calc_ma(third, diff)

    def plot(self):
        cleared_data = self.data[self.long - 1:]
        short_ma = get_ma(self.short).data
        long_ma = get_ma(self.long).data
        cleared_short = short_ma[self.long - 1:]
        cleared_long = long_ma[self.long - 1:]
        diff = cleared_long - cleared_short
        x_data = list(range(self.long - 1, len(self.data)))
        plt.plot(x_data, simulation.from_curr(cleared_short))
        plt.plot(x_data, simulation.from_curr(cleared_long))
        plt.subplot(212)
        plt.plot([0, len(self.data) - 1], [0, 0], color="red")
        plt.plot(x_data, simulation.from_curr(cleared_data))
        plt.plot(x_data, simulation.from_curr(diff))

    def requires_subplot(self):
        return True


class BalanceRecords(Indicator):

    def __init__(self, filename):
        Indicator.__init__(self)
        self.data = {}
        lines = []
        with open(filename, "r") as file:
            lines = file.readlines()
        current_name = None
        for line in lines:
            if line.startswith("ma"):
                current_name = f"ma {line.split()[1]} {line.split()[2]}"
                self.data[current_name] = []
            else:
                self.data[current_name].append(int(line))

    def get(filename):
        name = f"balancerec_{filename}"
        if name not in indicators:
            balancerec = BalanceRecords(filename)
            indicators[name] = balancerec
            return balancerec
        else:
            return indicators[name]

    def get_best(self, length, offset):
        averages = {}
        for ind_name in self.data:
            balance_record = self.data[ind_name]
            start = -length * 2 + offset
            end = start + length * 2
            balance_record_cut = balance_record[start:end]
            diff = np.diff(balance_record_cut)
            avg_diff = utils.moving_average(diff, length)
            avg_diff_cut = avg_diff[-length:]
            # plt.plot(avg_diff_cut)
            averages[ind_name] = np.mean(avg_diff_cut)
        # plt.show()
        # import sys
        # sys.exit()
        best = max(averages, key=averages.get)
        return best


@njit
def detect_cross(lst1, lst2, offset):
    v1 = lst1[offset]
    v2 = lst2[offset]
    v1p = lst1[offset - 1]
    v2p = lst2[offset - 1]
    lst1_not_above_lst2 = v1 - v2 <= 0
    it_was_above_lst2 = v1p - v2p > 0
    lst1_not_below_lst2 = v1 - v2 >= 0
    it_was_below_lst2 = v1p - v2p < 0
    cross_above = lst1_not_above_lst2 and it_was_above_lst2
    cross_below = lst1_not_below_lst2 and it_was_below_lst2
    return cross_above, cross_below


@njit
def zero_cross(lst, offset):
    v = lst[offset]
    vp = lst[offset - 1]
    lst1_not_above_zero = v <= 0
    it_was_above_zero = vp > 0
    lst1_not_below_zero = v >= 0
    it_was_below_zero = vp < 0
    cross_above = lst1_not_above_zero and it_was_above_zero
    cross_below = lst1_not_below_zero and it_was_below_zero
    return cross_above, cross_below
