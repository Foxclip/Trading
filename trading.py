import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d  # noqa
import simulation
from simulation import to_curr, from_curr
import numpy as np
import time


def surface_plot(x, y, z, xlabel="", ylabel=""):
    x, y = np.meshgrid(x, y)
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot_surface(x, y, z, cmap='plasma')
    plt.show()


if __name__ == "__main__":

    # settings
    simulation.precision = 5
    simulation.amount = 1000000

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
    sl_list = [25, 50, 75, 100, 150, 200, 350, 400, 450, 600]
    tp_list = sl_list[:]
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

    # bar plot
    x = np.array(sl_list[:])
    y = np.array(tp_list[:])
    balance_arr = np.array([from_curr(sim.balance, simulation.precision)
                            for sim
                            in simulation.simulations])
    z = balance_arr.reshape(len(tp_list), len(sl_list))
    surface_plot(x, y, z, xlabel="SL", ylabel="TP")

    # # plotting results
    # for sim in simulation.simulations:
    #     record = sim.balance_record
    #     precision = simulation.precision
    #     balance_record = from_curr(record, precision)
    #     plt.plot(balance_record, label=sim.name)
    # plt.legend(loc="upper right")
    # plt.show()
