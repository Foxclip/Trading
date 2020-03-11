from statistics import mean
import simulation


class Indicator:

    def __init__(self):
        self.record = []

    def step(self):
        raise NotImplementedError()


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length

    def step(self, offset):
        start = 0
        end = 0
        if(offset < self.length):
            start = 0
            end = offset + 1
        else:
            start = offset - self.length
            end = offset + 1
        value = mean(simulation.price_data[start:end])
        self.record.append(value)


def detect_cross(ma1, ma2):
    v1 = ma1.record[-1]
    v2 = ma2.record[-1]
    v1p = ma1.record[-2]
    v2p = ma2.record[-2]
    ma1_not_above_ma2 = v1 - v2 <= 0
    it_was_above_ma2 = v1p - v2p > 0
    ma1_not_below_ma2 = v1 - v2 >= 0
    it_was_below_ma2 = v1p - v2p < 0
    cross_above = ma1_not_above_ma2 and it_was_above_ma2
    cross_below = ma1_not_below_ma2 and it_was_below_ma2
    return cross_above, cross_below
