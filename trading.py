from mpl_toolkits import mplot3d  # noqa
import simulation
from simulation import to_curr
import plot


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
        "tp_range": 400,
        "leverage": 500,
        "name": "Untitled"
    }

    template = main_template.copy()
    template["name"] = "no_hedge 100 400"
    simulation.add_from_template(template)

    template = main_template.copy()
    template["hedge"] = True
    template["name"] = "hedge 100 400"
    simulation.add_from_template(template)

    template = main_template.copy()
    template["sl_range"] = 400
    template["tp_range"] = 100
    template["name"] = "no_hedge 400 100"
    simulation.add_from_template(template)

    template = main_template.copy()
    template["hedge"] = True
    template["sl_range"] = 400
    template["tp_range"] = 100
    template["name"] = "hedge 400 100"
    simulation.add_from_template(template)

    # running simulations
    simulation.run_all(["name", "hedge", "balance"])

    # balance plot
    plot.plot_balance()
