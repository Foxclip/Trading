from statistics import mean
import simulation
from queue import Queue


class Indicator:

    def __init__(self):
        self.record = []

    def step(self):
        raise NotImplementedError()


class MovingAverage(Indicator):

    def __init__(self, length):
        Indicator.__init__(self)
        self.length = length
        self.queue = Queue(maxsize=length)

    def step(self, offset):
        if self.queue.qsize() == self.queue.maxsize:
            self.queue.get()
        self.queue.put(simulation.price_data[offset])
        value = mean(self.queue.queue)
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
