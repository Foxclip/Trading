import simulation
from indicators import detect_cross, MovingAverage


def moving_averages(sim):

    gd = simulation.global_data

    # creating missing indicators
    ma1_name = f"ma{sim.ma1}"
    ma2_name = f"ma{sim.ma2}"
    if ma1_name not in gd.indicators:
        gd.indicators[ma1_name] = MovingAverage(sim.ma1)
    if ma2_name not in gd.indicators:
        gd.indicators[ma2_name] = MovingAverage(sim.ma2)

    if(sim.index > 0):  # skipping first bar

        # trading two moving averages
        ma1 = gd.indicators[f"ma{sim.ma1}"]
        ma2 = gd.indicators[f"ma{sim.ma2}"]

        # closing all orders before the weekend
        weekend_time = sim.dayofweek() == 4 and sim.hour() == 23
        if sim.weekend_closing and weekend_time:
            for order in sim.orders:
                sim.close_order(order)
            return

        # trading
        cross_above, cross_below = detect_cross(ma1.data, ma2.data,
                                                sim.index)
        if len(sim.orders) == 0:
            # yes, in reverse order
            if(cross_below):
                sim.sell(0.01, sl=sim.sl_range, tp=sim.tp_range)
            if(cross_above):
                sim.buy(0.01, sl=sim.sl_range, tp=sim.tp_range)
