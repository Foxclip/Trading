import pandas as pd
import matplotlib.pyplot as plt
import enum
from statistics import mean


def to_curr(amount, precision):
    return amount * 10**precision


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

    def __init__(self, price_data, starting_balance, ma_length):
        self.index = 0
        self.orders = []
        self.ma_record = []
        self.balance_record = []
        self.price_data = price_data
        self.balance = starting_balance
        self.ma_length = ma_length

    def price(self, lookback=0):
        return self.price_data[self.index - lookback]

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
        new_order = Order(amount, self.price(), OrderType.BUY)
        self.orders.append(new_order)
        print("BUY")
        # plt.scatter(self.index, self.price(), color="green")

    def sell(self, amount):
        new_order = Order(amount, self.price(), OrderType.SELL)
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
            f"Price: {from_curr(self.price(), 5)} "
            f"Balance: {from_curr(self.balance, 5)} "
            f"Equity: {from_curr(self.equity(), 5)} "
            f"FPL: {from_curr(self.floating_PL(), 5)} "
        )


if __name__ == "__main__":
    df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
    precision = 5
    eur_usd = [int(round(x * 10**precision, 0))
               for x in list(df["<CLOSE>"])[-10000:]]
    # plt.plot(eur_usd)
    simulation1 = Simulation(eur_usd, to_curr(1000, precision), 10)
    while(simulation1.advance()):
        pass
    # plt.plot(simulation.ma_record)
    plt.plot(from_curr(simulation1.balance_record, precision))
    plt.show()
