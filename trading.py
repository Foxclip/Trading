import pandas as pd
import matplotlib.pyplot as plt
import enum
from statistics import mean
import math


def to_curr(amount, precision):
    return int(round(amount * 10**precision))


def from_curr(object, precision):
    if isinstance(object, int):
        return object / 10**precision
    elif isinstance(object, list):
        return [x / 10**precision for x in object]


class OrderType(enum.Enum):
    BUY = 0
    SELL = 1


class Order:

    type = None
    amount = 0
    open_price = 0

    def __init__(self, amount, price, type):
        self.amount = amount
        self.open_price = price
        self.type = type

    def calculate_floating_PL(self, price):
        if self.type == OrderType.BUY:
            return self.amount * (price - self.open_price)
        else:
            return self.amount * (self.open_price - price)


class Simulation:

    def __init__(self, price_data, ask_price_data, bid_price_data,
                 starting_balance, ma_length, precision, ignore_spread=False):
        self.index = 0
        self.orders = []
        self.ma_record = []
        self.balance_record = []
        self.price_data = price_data
        self.ask_price_data = ask_price_data
        self.bid_price_data = bid_price_data
        self.balance = starting_balance
        self.ma_length = ma_length
        self.precision = precision
        self.ignore_spread = ignore_spread

    def price(self, lookback=0):
        return self.price_data[self.index - lookback]

    def ask_price(self, lookback=0):
        return self.ask_price_data[self.index - lookback]

    def bid_price(self, lookback=0):
        return self.bid_price_data[self.index - lookback]

    def floating_PL(self):
        return sum([order.calculate_floating_PL(self.price())
                    for order
                    in self.orders])

    def equity(self):
        return self.balance + self.floating_PL()

    def moving_average(self, length):
        if(self.index < length):
            return mean(self.price_data[0:self.index + 1])
        else:
            return mean(self.price_data[self.index - length:self.index + 1])

    def buy(self, amount):
        price = self.price() if self.ignore_spread else self.ask_price()
        new_order = Order(amount, price, OrderType.BUY)
        self.orders.append(new_order)
        print("BUY")
        # plt.scatter(self.index, self.price(), color="green")

    def sell(self, amount):
        price = self.price() if self.ignore_spread else self.bid_price()
        new_order = Order(amount, price, OrderType.SELL)
        self.orders.append(new_order)
        print("SELL")
        # plt.scatter(self.index, self.price(), color="blue")

    def close_order(self, order):
        self.balance += order.calculate_floating_PL(self.price())
        self.orders.remove(order)
        print("CLOSE")

    def advance(self):
        if self.index < len(self.price_data):
            self.record()
            self.output()
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

    def action(self):
        if(self.index > 0):
            # close
            price_not_above_ma = self.price() - self.ma_record[-1] <= 0
            it_was_above_ma = self.price(1) - self.ma_record[-2] > 0
            price_not_below_ma = self.price() - self.ma_record[-1] >= 0
            it_was_below_ma = self.price(1) - self.ma_record[-2] < 0
            cross_above = price_not_above_ma and it_was_above_ma
            cross_below = price_not_below_ma and it_was_below_ma
            if((len(self.orders) > 0) and (cross_above or cross_below)):
                self.close_order(self.orders[0])
            # buy
            price_above_ma = self.price() - self.ma_record[-1] > 0
            it_wasnt_above_ma = self.price(1) - self.ma_record[-2] <= 0
            if(price_above_ma and it_wasnt_above_ma):
                # self.buy(10)
                self.sell(10)
            # sell
            price_below_ma = self.price() - self.ma_record[-1] < 0
            it_wasnt_below_ma = self.price(1) - self.ma_record[-2] >= 0
            if(price_below_ma and it_wasnt_below_ma):
                # self.sell(10)
                self.buy(10)

    def output(self):
        print(
            f"Bar: {self.index} "
            f"Price: {from_curr(self.price(), self.precision)} "
            f"Balance: {from_curr(self.balance, self.precision)} "
            f"Equity: {from_curr(self.equity(), self.precision)} "
            f"FPL: {from_curr(self.floating_PL(), self.precision)} "
        )


if __name__ == "__main__":
    df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
    precision = 5
    amount = 100000
    eur_usd = [to_curr(x, precision) for x in list(df["<CLOSE>"])][-amount:]
    eur_usd_ask = []
    eur_usd_bid = []
    for bar_i in range(len(eur_usd)):
        price = eur_usd[bar_i]
        spread = df["<SPREAD>"][bar_i]
        spread_add = math.ceil(spread / 2)
        eur_usd_ask.append(eur_usd[bar_i] + spread_add)
        eur_usd_bid.append(eur_usd[bar_i] - spread_add)
    simulation1 = Simulation(eur_usd, eur_usd_ask, eur_usd_bid,
                             to_curr(1000, precision), 10, precision,
                             ignore_spread=True)
    simulation2 = Simulation(eur_usd, eur_usd_ask, eur_usd_bid,
                             to_curr(1000, precision), 10, precision,
                             ignore_spread=False)
    simulation1.run()
    simulation2.run()
    # plt.plot(simulation.ma_record)
    plt.plot(from_curr(simulation1.balance_record, precision))
    plt.plot(from_curr(simulation2.balance_record, precision))
    plt.show()
