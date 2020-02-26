import pandas as pd
import matplotlib.pyplot as plt
import enum


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

    def __init__(self, price_data, starting_balance):
        self.price_data = price_data
        self.balance = starting_balance

    def get_current_price(self):
        return self.price_data[self.index]

    def floating_PL(self):
        return sum([order.calculate_floating_PL(self.get_current_price())
                    for order
                    in self.orders])

    def equity(self):
        return self.balance + self.floating_PL()

    def buy(self, amount):
        new_order = Order(amount, self.get_current_price(), OrderType.BUY)
        self.orders.append(new_order)

    def sell(self, amount):
        new_order = Order(amount, self.get_current_price(), OrderType.SELL)
        self.orders.append(new_order)

    def close_order(self, order):
        self.balance += order.calculate_floating_PL(self.get_current_price())
        self.orders.remove(order)

    def advance(self):
        if self.index < len(self.price_data):
            self.output()
            self.action()
            self.index += 1
            return True
        else:
            return False

    def action(self):
        if(self.index == 0):
            self.buy(10)
        if(self.index == 10):
            self.close_order(self.orders[0])

    def output(self):
        print(
            f"Bar: {self.index} "
            f"Price: {self.get_current_price()} "
            f"Balance: {self.balance} "
            f"Equity: {self.equity()} "
            f"Floating PL: {self.floating_PL()}"
        )


if __name__ == "__main__":
    df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
    eur_usd = list(df["<CLOSE>"])[-100:]
    simulation = Simulation(eur_usd, 1000.0)
    while(simulation.advance()):
        pass


# plt.plot()
# plt.show()
