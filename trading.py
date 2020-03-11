from mpl_toolkits import mplot3d  # noqa
import simulation
from simulation import to_curr
import plot


if __name__ == "__main__":

    # settings
    simulation.precision = 5
    simulation.amount = 100000

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    main_template = {
        "balance": to_curr(100.0, simulation.precision),
        "ignore_spread": False,
        "sl_range": 100,
        "tp_range": 400,
        "ma1": 10,
        "ma2": 20,
        "leverage": 500,
        "name": "Untitled"
    }

    ma1lst = [1, 2, 4, 8, 16, 32, 64, 128]
    ma2lst = ma1lst[:]
    for ma2 in ma2lst:
        for ma1 in ma1lst:
            template = main_template.copy()
            template["name"] = f"{ma1} {ma2}"
            template["ma1"] = ma1
            template["ma2"] = ma2
            simulation.add_from_template(template)

    # running simulations
    simulation.run_all(["name", "hedge", "balance"])

    # balance plot
    plot.balance_surface_plot(ma1lst, ma2lst, xlabel="ma1", ylabel="ma2")
