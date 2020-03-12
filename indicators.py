import simulation
import utils


class Indicator:

    def __init__(self):
        self.data = []

    def calculate(self):
        raise NotImplementedError()

    def __getitem__(self, offset):
        return self.data[offset]


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length
        self.data = utils.moving_average(simulation.price_data, self.length)


def detect_cross(ma1, ma2, offset):
    v1 = ma1[offset - 1]
    v2 = ma2[offset - 1]
    v1p = ma1[offset - 2]
    v2p = ma2[offset - 2]
    ma1_not_above_ma2 = v1 - v2 <= 0
    it_was_above_ma2 = v1p - v2p > 0
    ma1_not_below_ma2 = v1 - v2 >= 0
    it_was_below_ma2 = v1p - v2p < 0
    cross_above = ma1_not_above_ma2 and it_was_above_ma2
    cross_below = ma1_not_below_ma2 and it_was_below_ma2
    return cross_above, cross_below
