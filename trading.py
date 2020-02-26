import pandas as pd
import matplotlib.pyplot as plt
import enum
from statistics import mean


class OrderType(enum.Enum):
    BUY = 0
    SELL = 1


class Order:

    type = None
    amount = 0.0
    open_price = 0.0

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

    index = 0
    orders = []
    price_data = None
    balance = 0.0
    ma_record = []
    balance_record = []

    def __init__(self, price_data, starting_balance):
        self.price_data = price_data
        self.balance = starting_balance

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

    def sell(self, amount):
        new_order = Order(amount, self.price(), OrderType.SELL)
        self.orders.append(new_order)
        print("SELL")

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
        self.ma_record.append(self.moving_average(10))
        self.balance_record.append(self.balance)

    def action(self):
        if(self.index > 0):
            # close
            price_not_above_ma = self.price() - self.ma_record[-1] <= 0
            it_was_above_ma = self.price(1) - self.ma_record[-2] > 0
            price_not_below_ma = self.price() - self.ma_record[-1] >= 0
            it_was_below_ma = self.price(1) - self.ma_record[-2] < 0
            cross_from_above = price_not_above_ma and it_was_above_ma
            cross_from_below = price_not_below_ma and it_was_below_ma
            if(cross_from_above or cross_from_below):
                self.close_order(self.orders[0])
            # buy
            price_above_ma = self.price() - self.ma_record[-1] > 0
            it_wasnt_above_ma = self.price(1) - self.ma_record[-2] <= 0
            if(price_above_ma and it_wasnt_above_ma):
                self.buy(10)
            # sell
            price_below_ma = self.price() - self.ma_record[-1] < 0
            it_wasnt_below_ma = self.price(1) - self.ma_record[-2] >= 0
            if(price_below_ma and it_wasnt_below_ma):
                self.sell(10)

    def output(self):
        print(
            f"Bar: {self.index} "
            f"Price: {self.price()} "
            f"Balance: {self.balance} "
            f"Equity: {self.equity()} "
            f"FPL: {self.floating_PL()} "
        )


if __name__ == "__main__":
    df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
    eur_usd = list(df["<CLOSE>"])[-100000:]
    simulation = Simulation(eur_usd, 1000.0)
    while(simulation.advance()):
        pass
    # plt.plot(eur_usd)
    # plt.plot(simulation.ma_record)
    plt.plot(simulation.balance_record)
    plt.show()
