import simulation
import utils
from numba import njit


class Indicator:

    def __init__(self):
        self.data = []

    def calculate(self):
        raise NotImplementedError()


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length
        self.data = utils.moving_average(simulation.global_data.price_data,
                                         self.length)


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
