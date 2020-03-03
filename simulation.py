import matplotlib.pyplot as plt
import enum
from statistics import mean

plot_orders = False
precision = 5
amount = 1000000


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

    def __init__(self, amount, price, type, stop_loss=0, take_profit=0):
        self.amount = amount
        self.open_price = price
        self.type = type
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def calculate_floating_PL(self, price):
        if self.type == OrderType.BUY:
            return self.amount * (price - self.open_price)
        else:
            return self.amount * (self.open_price - price)

    def should_close(self, price):
        SL_hit = False
        TP_hit = False
        if self.type == OrderType.BUY:
            SL_hit = (self.stop_loss > 0 and price <= self.stop_loss)
            TP_hit = (self.take_profit > 0 and price >= self.take_profit)
        elif self.type == OrderType.SELL:
            SL_hit = (self.stop_loss > 0 and price >= self.stop_loss)
            TP_hit = (self.take_profit > 0 and price <= self.take_profit)
        if(SL_hit):
            print("SL_hit")
        if(TP_hit):
            print("TP_hit")
        return SL_hit or TP_hit


class Simulation:

    def __init__(self, price_data, ask_price_data, bid_price_data,
                 starting_balance, ma_length, precision, ignore_spread=False,
                 put_stops=False, sl_range=20, tp_range=20, name="Untitled"):
        self.index = 0
        self.orders = []
        self.order_count = 0
        self.ma_record = []
        self.balance_record = []
        self.price_data = price_data
        self.ask_price_data = ask_price_data
        self.bid_price_data = bid_price_data
        self.balance = starting_balance
        self.ma_length = ma_length
        self.precision = precision
        self.ignore_spread = ignore_spread
        self.put_stops = put_stops
        self.sl_range = sl_range
        self.tp_range = tp_range
        self.name = name

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

    def buy(self, amount, stop_loss=0, take_profit=0):
        price = self.price() if self.ignore_spread else self.ask_price()
        new_order = Order(amount, price, OrderType.BUY,
                          stop_loss, take_profit)
        self.orders.append(new_order)
        print("BUY")
        if plot_orders:
            plt.scatter(self.index, self.price(), color="green")
            if not self.ignore_spread:
                plt.scatter(self.index, price, color="green")
        self.order_count += 1

    def sell(self, amount, stop_loss=0, take_profit=0):
        price = self.price() if self.ignore_spread else self.bid_price()
        new_order = Order(amount, price, OrderType.SELL,
                          stop_loss, take_profit)
        self.orders.append(new_order)
        print("SELL")
        if plot_orders:
            plt.scatter(self.index, price, color="blue")
        self.order_count += 1

    def close_order(self, order):
        self.balance += order.calculate_floating_PL(self.price())
        self.orders.remove(order)
        print("CLOSE")
        if plot_orders:
            plt.scatter(self.index, self.price(), color="black")

    def advance(self):
        if self.index < len(self.price_data):
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
                        self.sell(10,
                                  stop_loss=self.price() + self.sl_range,
                                  take_profit=self.price() - self.tp_range)
                    else:
                        self.sell(10)
            # buy
            if len(self.orders) == 0 or not self.put_stops:
                price_below_ma = self.price() - self.ma_record[-1] < 0
                it_wasnt_below_ma = self.price(1) - self.ma_record[-2] >= 0
                if(price_below_ma and it_wasnt_below_ma):
                    if(self.put_stops):
                        self.buy(10,
                                 stop_loss=self.price() - self.sl_range,
                                 take_profit=self.price() + self.tp_range)
                    else:
                        self.buy(10)

    def output(self):
        print(
            f"Name: {self.name} "
            f"Bar: {self.index} "
            f"Price: {from_curr(self.price(), self.precision)} "
            f"Balance: {from_curr(self.balance, self.precision)} "
            f"Equity: {from_curr(self.equity(), self.precision)} "
            f"FPL: {from_curr(self.floating_PL(), self.precision)} "
        )
