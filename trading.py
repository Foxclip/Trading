from mpl_toolkits import mplot3d  # noqa
import simulation
from simulation import to_curr
import time
import plot


if __name__ == "__main__":

    # settings
    simulation.precision = 5
    simulation.amount = 10000

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    main_template = {
        "balance": to_curr(100.0, simulation.precision),
        "ma_length": 15,
        "ignore_spread": False,
        "put_stops": True,
        "sl_range": 100,
        "tp_range": 500,
        "leverage": 500,
        "name": "Untitled"
    }
    sl_list = [400, 500]
    tp_list = [50, 75, 100, 150, 200]
    for tp in tp_list:
        for sl in sl_list:
            template = main_template.copy()
            template["sl_range"] = sl
            template["tp_range"] = tp
            template["name"] = f"sl{sl} tp{tp}"
            simulation.add_from_template(template)

    # running simulations
    time1 = time.time()
    simulation.run_all()
    time2 = time.time()
    time_passed = time2 - time1
    print(f"Time: {time_passed}s")

    # balance surface plot
    plot.balance_surface_plot(x=sl_list, y=tp_list, xlabel="SL", ylabel="TP")

    # balance plot
    plot.plot_balance()
