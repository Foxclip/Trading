import pandas as pd
import enum
import math
import time
import os
import multiprocessing
import itertools
from numba import njit
import utils
from strategies import moving_averages


simulations = []


class GlobalSettings:
    precision = 5
    amount = 1000000
    step_output = False
    order_output = False
    neg_balance = True
    lot_size = 100000
    record_balance = True


global_settings = GlobalSettings()


class GlobalData:
    price_data = None
    ask_data = None
    bid_data = None
    dayofweek_data = None
    hour_data = None
    minute_data = None
    indicators = {}
    prop_list = []


global_data = GlobalData()


@njit
def _to_curr(lst, precision):
    return [int(round(x * 10**precision)) for x in lst]


def to_curr(object):
    if isinstance(object, float):
        return int(round(object * 10**global_settings.precision))
    elif isinstance(object, list):
        return _to_curr(utils.to_typed_list(object), global_settings.precision)
    else:
        obj_type = type(global_settings.amount)
        raise Exception(f"{obj_type} is not allowed in to_curr")


def from_curr(object):
    if isinstance(object, int):
        return object / 10**global_settings.precision
    elif isinstance(object, list):
        return [x / 10**global_settings.precision for x in object]
    else:
        raise Exception(f"{type(object)} should not be in from_curr")


def calculate_margin(amount, price, leverage):
    return int(amount * from_curr(price)) // leverage


def generate_file(path, df):
    print("Generating file")
    price_data = to_curr(list(df["<CLOSE>"]))
    ask_data = []
    bid_data = []
    for bar_i in range(len(price_data)):
        if(bar_i % 1000 == 0):
            percent = round(bar_i / len(price_data) * 100, 1)
            print(f"{bar_i}/{len(price_data)} ({percent}%)", end='\r')
        price = price_data[bar_i]
        spread = df["<SPREAD>"][bar_i]
        spread_half = math.ceil(spread / 2)
        ask_data.append(price + spread_half)
        bid_data.append(price - spread_half)
    print()
    print("Converting timestamps")
    combined_datetime = df["<DATE>"] + " " + df["<TIME>"]
    timestamps = pd.to_datetime(combined_datetime)
    print("Creating columns")
    df["ASK"] = from_curr(ask_data)
    df["BID"] = from_curr(bid_data)
    df["DAYOFWEEK"] = timestamps.dt.dayofweek
    df["HOUR"] = timestamps.dt.hour
    df["MINUTE"] = timestamps.dt.minute
    df = df.filter(["<CLOSE>", "ASK", "BID", "DAYOFWEEK", "HOUR", "MINUTE"])
    print("Saving to file")
    df.to_csv(path, index=False, sep="\t")
    return df


def load_file(path):
    print("Reading CSV")
    path_name, path_ext = os.path.splitext(path)
    generated_path = f"{path_name}_gen{path_ext}"
    df = None
    try:
        df = pd.read_csv(generated_path, sep="\t")
    except FileNotFoundError:
        df = pd.read_csv(path, sep="\t")
        df = generate_file(generated_path, df)
    amount = global_settings.amount
    global_data.price_data = to_curr(list(df["<CLOSE>"]))[-amount:]
    global_data.ask_data = to_curr(list(df["ASK"])[-amount:])
    global_data.bid_data = to_curr(list(df["BID"])[-amount:])
    global_data.dayofweek_data = list(df["DAYOFWEEK"])[-amount:]
    global_data.hour_data = list(df["HOUR"])[-amount:]
    global_data.minute_data = list(df["MINUTE"])[-amount:]


def add_from_template(template):
    new_sim = Simulation()
    for key in template.keys():
        setattr(new_sim, key, template[key])
    simulations.append(new_sim)


def _global_init(p_global_settings, p_global_data):
    print(f"Starting process {multiprocessing.current_process().name}")
    global global_settings, global_data
    global_settings = p_global_settings
    global_data = p_global_data


def _run_simulation(sim):
    sim.run()
    if global_data.prop_list:
        sim.print_props(global_data.prop_list)
    return sim


def run_all(p_prop_list=[], jobs=None):
    print("Running simulations")
    global_data.prop_list = p_prop_list
    time1 = time.time()
    if jobs is None or jobs > 1:
        with multiprocessing.Pool(
            jobs,
            _global_init,
            (global_settings, global_data)
        ) as pool:
            global simulations
            simulations = pool.map(_run_simulation, simulations)
    else:
        for sim in simulations:
            _run_simulation(sim)
    time2 = time.time()
    time_passed = time2 - time1
    print(f"Time: {time_passed}s")


def create_grid(lists, f):
    if len(lists) <= 1:
        raise ValueError("Should be at least two lists")
    elif len(lists) == 2:
        for l2 in lists[1]:
            for l1 in lists[0]:
                f(l1, l2)
    else:
        for combination in itertools.product(*lists):
            f(*combination)


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
        return int(round(self.amount * from_curr(pricediff),
                         global_settings.precision))

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
        if global_settings.order_output:
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
                 sl_range=20, tp_range=20, ma1=1, ma2=10, leverage=500,
                 hedge=False, weekend_closing=False, name="Untitled"):
        self.index = 0
        self.orders = []
        self.balance_record = []
        self.balance = to_curr(balance)
        self.ignore_spread = ignore_spread
        self.sl_range = sl_range
        self.tp_range = tp_range
        self.ma1 = ma1
        self.ma2 = ma2
        self.leverage = leverage
        self.hedge = hedge
        self.weekend_closing = weekend_closing
        self.name = name

    def price(self, lookback=0):
        return global_data.price_data[self.index - lookback]

    def ask_price(self, lookback=0):
        return global_data.ask_data[self.index - lookback]

    def bid_price(self, lookback=0):
        return global_data.bid_data[self.index - lookback]

    def floating_PL(self):
        return sum([order.calculate_floating_PL(self.price())
                    for order
                    in self.orders])

    def equity(self):
        return self.balance + self.floating_PL()

    def used_margin(self):
        return sum([order.margin(self.price(), self.leverage)
                    for order
                    in self.orders])

    def free_margin(self):
        return self.equity() - self.used_margin()

    def dayofweek(self):
        return global_data.dayofweek_data[self.index]

    def hour(self):
        return global_data.hour_data[self.index]

    def minute(self):
        return global_data.minute_data[self.index]

    def _buy_or_sell(self, lots, stop_loss, take_profit, order_type):
        if order_type == OrderType.BUY:
            bid_or_ask_price = self.ask_price()
            str = "BUY"
        elif order_type == OrderType.SELL:
            bid_or_ask_price = self.bid_price()
            str = "SELL"
        price = self.price() if self.ignore_spread else bid_or_ask_price
        amount = to_curr(lots * global_settings.lot_size)
        margin = calculate_margin(amount, price, self.leverage)
        if not global_settings.neg_balance and margin > self.free_margin():
            raise Exception(f"Not enough free margin to {str}")
        new_order = Order(amount, price, order_type, stop_loss, take_profit)
        self.orders.append(new_order)
        if global_settings.order_output:
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
        if global_settings.order_output:
            print("CLOSE")

    def advance(self):
        if self.index < len(global_data.price_data):
            self.record()
            self.output()
            self.SLTP()
            self.action()
            self.index += 1
            return True
        else:
            return False

    def init(self):
        pass

    def run(self):
        self.init()
        while(self.advance()):
            pass

    def record(self):
        if global_settings.record_balance:
            self.balance_record.append(self.balance)
        pass

    def SLTP(self):
        for order_i in range(len(self.orders) - 1, -1, -1):
            if(self.orders[order_i].should_close(self.price())):
                self.close_order(self.orders[order_i])
                if global_settings.order_output:
                    print("___SLTP___")

    def action(self):
        moving_averages(self)

    def output(self):
        if global_settings.step_output:
            print(
                f"Name: {self.name} "
                f"Bar: {self.index} "
                f"Price: {from_curr(self.price())} "
                f"Balance: {from_curr(self.balance)} "
                f"Equity: {from_curr(self.equity())} "
                f"FPL: {from_curr(self.floating_PL())} "
                f"um: {from_curr(self.used_margin())} "
                f"fm: {from_curr(self.free_margin())}"
            )

    def get_prop_str(self, prop_list):
        result = ""
        for prop_name in prop_list:
            prop_value = getattr(self, prop_name)
            if prop_name == "balance":
                prop_value = from_curr(self.balance)
            if prop_name == "name":
                result += f"{prop_value} "
                continue
            result += f"{prop_name}:{prop_value} "
        return result

    def print_props(self, prop_list):
        print(self.get_prop_str(prop_list))
