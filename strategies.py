from indicators import detect_cross, zero_cross
from indicators import get_ma, get_macd


def _weekend_close(sim):
    weekend_time = sim.dayofweek() == 4 and sim.hour() == 23
    if sim.weekend_closing and weekend_time:
        for order in sim.orders:
            sim.close_order(order)
        return True
    return False


def moving_averages(sim):

    if(sim.index > 0):  # skipping first bar

        # getting indicators
        ma1 = get_ma(sim.ma1)
        ma2 = get_ma(sim.ma2)

        # closing all orders before the weekend
        if _weekend_close(sim):
            return

        # trading
        cross_above, cross_below = detect_cross(ma1.data, ma2.data, sim.index)
        if len(sim.orders) == 0:
            # yes, in reverse order
            if(cross_below):
                sim.sell(0.01, sl=sim.sl_range, tp=sim.tp_range)
            if(cross_above):
                sim.buy(0.01, sl=sim.sl_range, tp=sim.tp_range)


def macd(sim):

    # getting indicators
    macd = get_macd(sim.macd_s, sim.macd_l, sim.macd_t)

    # closing all orders before the weekend
    if _weekend_close(sim):
        return

    # trading
    cross_above, cross_below = zero_cross(macd.data, sim.index)
    if len(sim.orders) == 0:
        if(cross_below):
            sim.buy(0.01, sl=sim.sl_range, tp=sim.tp_range)
        if(cross_above):
            sim.sell(0.01, sl=sim.sl_range, tp=sim.tp_range)
