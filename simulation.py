import pandas as pd
import enum
from statistics import mean
import math
import time

precision = 5
amount = 1000000
step_output = False
order_output = False
neg_balance = True
lot_size = 100000
price_data = None
ask_data = None
bid_data = None
simulations = []


def to_curr(amount, precision):
    if isinstance(amount, float):
        return int(round(amount * 10**precision))
    else:
        raise Exception(f"{type(amount)} should not be in to_curr")


def from_curr(object, precision):
    if isinstance(object, int):
        return object / 10**precision
    elif isinstance(object, list):
        return [x / 10**precision for x in object]
    else:
        raise Exception(f"{type(object)} should not be in from_curr")


def calculate_margin(amount, price, leverage):
    return int(amount * from_curr(price, precision)) // leverage


def load_file(path):

    print("Reading CSV")
    df = pd.read_csv(path, sep="\t")

    print("Generating bid/ask data")
    price_data_raw = list(df["<CLOSE>"])
    global price_data, ask_data, bid_data
    price_data = [to_curr(x, precision) for x in price_data_raw][-amount:]
    ask_data = []
    bid_data = []
    for bar_i in range(len(price_data)):
        price = price_data[bar_i]
        spread = df["<SPREAD>"][bar_i]
        spread_half = math.ceil(spread / 2)
        ask_data.append(price + spread_half)
        bid_data.append(price - spread_half)


def add_from_template(template):
    new_sim = Simulation()
    for key in template.keys():
        setattr(new_sim, key, template[key])
    simulations.append(new_sim)


def run_all(print_props=[]):
    print("Running simulations")
    time1 = time.time()
    for sim in simulations:
        sim.run()
        if print_props:
            for prop_name in print_props:
                prop_value = getattr(sim, prop_name)
                if prop_name == "balance":
                    prop_value = from_curr(sim.balance, precision)
                if prop_name == "name":
                    print(f"{prop_value}", end=' ')
                    continue
                print(f"{prop_name}:{prop_value}", end=' ')
            print()
    time2 = time.time()
    time_passed = time2 - time1
    print(f"Time: {time_passed}s")


class OrderType(enum.Enum):
    BUY = 0
    SELL = 1


class Order:

    def __init__(self, amount, open_price, type, stop_loss=0, take_profit=0):
        self.amount = amount
        self.open_price = open_price
        self.type = type
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.hedging_order = None

    def calculate_floating_PL(self, price):
        pricediff = 0
        if self.type == OrderType.BUY:
            pricediff = price - self.open_price
        else:
            pricediff = self.open_price - price
        return int(self.amount * from_curr(pricediff, precision))

    def margin(self, price, leverage):
        return calculate_margin(self.amount, price, leverage)

    def should_close(self, price):
        SL_hit = False
        TP_hit = False
        if self.type == OrderType.BUY:
            SL_hit = (self.stop_loss > 0 and price <= self.stop_loss)
            TP_hit = (self.take_profit > 0 and price >= self.take_profit)
        elif self.type == OrderType.SELL:
            SL_hit = (self.stop_loss > 0 and price >= self.stop_loss)
            TP_hit = (self.take_profit > 0 and price <= self.take_profit)
        result = SL_hit or TP_hit
        if order_output:
            if result:
                print(f"type {self.type} "
                      f"sl {self.stop_loss} "
                      f"tp {self.take_profit}")
            if(SL_hit):
                print("SL_hit")
            if(TP_hit):
                print("TP_hit")
        return result


class Simulation:

    def __init__(self, balance=0.0, ma_length=10, ignore_spread=False,
                 put_stops=False, sl_range=20, tp_range=20, leverage=500,
                 hedge=False, name="Untitled"):
        self.index = 0
        self.orders = []
        self.ma_record = []
        self.balance_record = []
        self.balance = to_curr(balance, precision)
        self.ma_length = ma_length
        self.ignore_spread = ignore_spread
        self.put_stops = put_stops
        self.sl_range = sl_range
        self.tp_range = tp_range
        self.name = name
        self.leverage = leverage
        self.hedge = hedge

    def price(self, lookback=0):
        return price_data[self.index - lookback]

    def ask_price(self, lookback=0):
        return ask_data[self.index - lookback]

    def bid_price(self, lookback=0):
        return bid_data[self.index - lookback]

    def floating_PL(self):
        return sum([order.calculate_floating_PL(self.price())
                    for order
                    in self.orders])

    def equity(self):
        return self.balance + self.floating_PL()

    def moving_average(self, length):
        if(self.index < length):
            return mean(price_data[0:self.index + 1])
        else:
            return mean(price_data[self.index - length:self.index + 1])

    def used_margin(self):
        return sum([order.margin(self.price(), self.leverage)
                    for order
                    in self.orders])

    def free_margin(self):
        return self.equity() - self.used_margin()

    def _buy_or_sell(self, lots, stop_loss, take_profit, order_type):
        if order_type == OrderType.BUY:
            bid_or_ask_price = self.ask_price()
            str = "BUY"
        elif order_type == OrderType.SELL:
            bid_or_ask_price = self.bid_price()
            str = "SELL"
        price = self.price() if self.ignore_spread else bid_or_ask_price
        amount = to_curr(lots * lot_size, precision)
        margin = calculate_margin(amount, price, self.leverage)
        if not neg_balance and margin > self.free_margin():
            raise Exception(f"Not enough free margin to {str}")
        new_order = Order(amount, price, order_type, stop_loss, take_profit)
        self.orders.append(new_order)
        if order_output:
            print(str)
        return new_order

    def buy(self, lots, sl=0, tp=0):
        stop_loss = self.price() - sl
        take_profit = self.price() + tp
        order = self._buy_or_sell(lots, stop_loss, take_profit, OrderType.BUY)
        hedge_sl = 0
        hedge_tp = 0
        if self.hedge:
            if tp > sl:
                hedge_sl = self.price() + sl
            else:
                hedge_sl = self.price() + tp / 2
            hedge_tp = self.price() - sl
            order.hedging_order = self._buy_or_sell(lots, hedge_sl, hedge_tp,
                                                    OrderType.SELL)

    def sell(self, lots, sl=0, tp=0):
        stop_loss = self.price() + sl
        take_profit = self.price() - tp
        order = self._buy_or_sell(lots, stop_loss, take_profit, OrderType.SELL)
        hedge_sl = 0
        hedge_tp = 0
        if self.hedge:
            if tp > sl:
                hedge_sl = self.price() - sl
            else:
                hedge_sl = self.price() - tp / 2
            hedge_tp = self.price() + sl
            order.hedging_order = self._buy_or_sell(lots, hedge_sl, hedge_tp,
                                                    OrderType.BUY)

    def close_order(self, order):
        self.balance += order.calculate_floating_PL(self.price())
        self.orders.remove(order)
        if order_output:
            print("CLOSE")

    def advance(self):
        if self.index < len(price_data):
            self.record()
            self.output()
            self.SLTP()
            self.action()
            self.index += 1
            return True
        else:
            return False

    def run(self):
        while(self.advance()):
            pass

    def record(self):
        self.ma_record.append(self.moving_average(self.ma_length))
        self.balance_record.append(self.balance)

    def SLTP(self):
        for order_i in range(len(self.orders) - 1, -1, -1):
            if(self.orders[order_i].should_close(self.price())):
                self.close_order(self.orders[order_i])
                if order_output:
                    print("___SLTP___")

    def action(self):
        if(self.index > 0):
            # close
            if not self.put_stops:
                price_not_above_ma = self.price() - self.ma_record[-1] <= 0
                it_was_above_ma = self.price(1) - self.ma_record[-2] > 0
                price_not_below_ma = self.price() - self.ma_record[-1] >= 0
                it_was_below_ma = self.price(1) - self.ma_record[-2] < 0
                cross_above = price_not_above_ma and it_was_above_ma
                cross_below = price_not_below_ma and it_was_below_ma
                if((len(self.orders) > 0) and (cross_above or cross_below)):
                    self.close_order(self.orders[0])
            # sell
            if len(self.orders) == 0 or not self.put_stops:
                price_above_ma = self.price() - self.ma_record[-1] > 0
                it_wasnt_above_ma = self.price(1) - self.ma_record[-2] <= 0
                if(price_above_ma and it_wasnt_above_ma):
                    if self.put_stops:
                        self.sell(0.01, sl=self.sl_range, tp=self.tp_range)
                    else:
                        self.sell(0.01)
            # buy
            if len(self.orders) == 0 or not self.put_stops:
                price_below_ma = self.price() - self.ma_record[-1] < 0
                it_wasnt_below_ma = self.price(1) - self.ma_record[-2] >= 0
                if(price_below_ma and it_wasnt_below_ma):
                    if(self.put_stops):
                        self.buy(0.01, sl=self.sl_range, tp=self.tp_range)
                    else:
                        self.buy(0.01)

    def output(self):
        if step_output:
            print(
                f"Name: {self.name} "
                f"Bar: {self.index} "
                f"Price: {from_curr(self.price(), precision)} "
                f"Balance: {from_curr(self.balance, precision)} "
                f"Equity: {from_curr(self.equity(), precision)} "
                f"FPL: {from_curr(self.floating_PL(), precision)} "
                f"um: {from_curr(self.used_margin(), precision)} "
                f"fm: {from_curr(self.free_margin(), precision)}"
            )
