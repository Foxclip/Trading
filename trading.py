import pandas as pd
import matplotlib.pyplot as plt
import math
import simulation
from simulation import from_curr, to_curr, Simulation


if __name__ == "__main__":
    df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
    plot_orders = False
    precision = 5
    amount = 10000
    simulation.plot_orders = plot_orders
    simulation.precision = precision
    simulation.amount = amount
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
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=400, name="100_400")
    simulation2 = Simulation(eur_usd, eur_usd_ask, eur_usd_bid,
                             to_curr(1000, precision), 10, precision,
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=500, name="100_500")
    simulation3 = Simulation(eur_usd, eur_usd_ask, eur_usd_bid,
                             to_curr(1000, precision), 10, precision,
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=600, name="100_600")
    simulation1.run()
    simulation2.run()
    simulation3.run()
    print(f"Sim 1 order count: {simulation1.order_count}")
    print(f"Sim 2 order count: {simulation2.order_count}")
    print(f"Sim 3 order count: {simulation3.order_count}")
    if plot_orders:
        plt.plot(eur_usd)
        plt.plot(simulation1.ma_record)
    else:
        balance_record1 = from_curr(simulation1.balance_record, precision)
        plt.plot(balance_record1, label=simulation1.name)
        balance_record2 = from_curr(simulation2.balance_record, precision)
        plt.plot(balance_record2, label=simulation2.name)
        balance_record3 = from_curr(simulation3.balance_record, precision)
        plt.plot(balance_record3, label=simulation3.name)
    plt.legend(loc="upper right")
    plt.show()
