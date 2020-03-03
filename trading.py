import matplotlib.pyplot as plt
import simulation
from simulation import from_curr, Simulation


if __name__ == "__main__":
    simulation.plot_orders = False
    simulation.precision = 5
    simulation.amount = 10000
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")
    simulation1 = Simulation(starting_balance=1000, ma_length=10,
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=400, name="100_400")
    simulation2 = Simulation(starting_balance=1000, ma_length=10,
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=500, name="100_500")
    simulation3 = Simulation(starting_balance=1000, ma_length=10,
                             ignore_spread=False, put_stops=True,
                             sl_range=100, tp_range=600, name="100_600")
    simulation1.run()
    simulation2.run()
    simulation3.run()
    print(f"Sim 1 order count: {simulation1.order_count}")
    print(f"Sim 2 order count: {simulation2.order_count}")
    print(f"Sim 3 order count: {simulation3.order_count}")
    if simulation.plot_orders:
        plt.plot(simulation.curr_record)
        plt.plot(simulation1.ma_record)
    else:
        record = simulation1.balance_record
        precision = simulation.precision
        balance_record1 = from_curr(record, precision)
        plt.plot(balance_record1, label=simulation1.name)
        record = simulation2.balance_record
        precision = simulation.precision
        balance_record2 = from_curr(record, precision)
        plt.plot(balance_record2, label=simulation2.name)
        record = simulation3.balance_record
        precision = simulation.precision
        balance_record3 = from_curr(record, precision)
        plt.plot(balance_record3, label=simulation3.name)
    plt.legend(loc="upper right")
    plt.show()
