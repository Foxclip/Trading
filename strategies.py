from indicators import detect_cross, zero_cross
from indicators import get_ma, get_macd, BalanceRecords
from simulation import Direction


def _weekend_close(sim):
    weekend_time = sim.dayofweek() == 4 and sim.hour() == 23
    if sim.weekend_closing and weekend_time:
        for order in sim.orders:
            sim.close_order(order)
        return True
    return False


def _trade(sim, cross_above, cross_below):
    normal_below = cross_below and sim.direction == Direction.NORMAL
    normal_above = cross_above and sim.direction == Direction.NORMAL
    reverse_below = cross_below and sim.direction == Direction.REVERSE
    reverse_above = cross_above and sim.direction == Direction.REVERSE
    if(normal_below or reverse_above):
        sim.buy(0.01, sl=sim.sl_range, tp=sim.tp_range)
    if(normal_above or reverse_below):
        sim.sell(0.01, sl=sim.sl_range, tp=sim.tp_range)


def moving_averages(sim):

    # getting indicators
    ma1 = get_ma(sim.ma1)
    ma2 = get_ma(sim.ma2)
    sim.indicators["ma1"] = ma1
    sim.indicators["ma2"] = ma2

    # skipping if moving averages are not "filled" yet
    if sim.index < max(ma1.length, ma2.length) + 1:
        return

    # closing all orders before the weekend
    if _weekend_close(sim):
        return

    # trading
    cross_above, cross_below = detect_cross(ma1.data, ma2.data, sim.index)
    if len(sim.orders) == 0:
        _trade(sim, cross_above, cross_below)


def macd(sim):

    # getting indicators
    macd = get_macd(sim.macd_s, sim.macd_l, sim.macd_t)
    sim.indicators["macd"] = macd

    # skipping if moving averages are not "filled" yet
    if sim.index < max(macd.long, macd.third) + 1:
        return

    # closing all orders before the weekend
    if _weekend_close(sim):
        return

    # trading
    cross_above, cross_below = zero_cross(macd.data, sim.index)
    if len(sim.orders) == 0:
        _trade(sim, cross_above, cross_below)


def balance_records(sim):

    # skipping if moving averages are not "filled" yet
    if sim.index < sim.brlen:
        return

    # getting indicators
    balance_records = BalanceRecords.get(sim.ma_record)

    # closing all orders before the weekend
    if _weekend_close(sim):
        return

    best = balance_records.get_best(sim.brlen, sim.index)
    ma1 = best.split()[1]
    ma2 = best.split()[2]
    sim.ma1 = int(ma1)
    sim.ma2 = int(ma2)
    moving_averages(sim)


def balancetime(sim):

    # skipping if moving averages are not "filled" yet
    if sim.index < sim.brlen:
        return

    # getting indicators
    ma_record = BalanceRecords.get(sim.ma_record)
    br_record = BalanceRecords.get(sim.br_record)

    # closing all orders before the weekend
    if _weekend_close(sim):
        return

    best_br = br_record.get_best(sim.brlen, sim.index)
    best_time = int(best_br.split()[1])
    best_ma = ma_record.get_best(best_time, sim.index)
    ma1 = best_ma.split()[1]
    ma2 = best_ma.split()[2]
    sim.ma1 = int(ma1)
    sim.ma2 = int(ma2)
    moving_averages(sim)
