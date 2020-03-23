import simulation
from simulation import to_curr
import plot
import sys


def single_sim(template, diff=None, resolution=None):
    simulation.global_settings.record_balance = True
    simulation.add_from_template(template)
    simulation.run_all(jobs=1)
    if len(sys.argv) == 1 or sys.argv[1] != "--noplot":
        plot.plot_balance(diff=diff, resolution=resolution)


def grid_search(f, lst1, lst2, xlabel, ylabel):
    simulation.global_settings.record_balance = False
    simulation.create_grid(lst1, lst2, f)
    simulation.run_all(["name", "balance"], jobs=None)
    if len(sys.argv) == 1 or sys.argv[1] != "--noplot":
        plot.balance_surface_plot(lst1, lst2, xlabel=xlabel, ylabel=ylabel)


if __name__ == "__main__":

    # settings
    simulation.global_settings.precision = 5
    simulation.global_settings.amount = 10**6

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    main_template = {
        "balance": to_curr(100.0),
        "ignore_spread": False,
        "sl_range": 400,
        "tp_range": 100,
        "ma1": 21,
        "ma2": 32,
        "leverage": 500,
        "name": "Untitled"
    }

    # # creating simulations
    # def create_sim(ma1, ma2):
    #     template = main_template.copy()
    #     template["name"] = f"{ma1} {ma2}"
    #     template["ma1"] = ma1
    #     template["ma2"] = ma2
    #     simulation.add_from_template(template)
    # grid_search(
    #     create_sim,
    #     list(range(1, 41)), list(range(1, 41)),
    #     "ma1", "ma2"
    # )

    single_sim(main_template)
