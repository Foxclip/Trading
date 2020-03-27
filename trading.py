import simulation
from simulation import to_curr
import plot
import sys


def sim_list(template_list, diff=None, resolution=None):
    # settings
    simulation.global_settings.record_balance = True
    # creating simulations
    for template in template_list:
        simulation.add_from_template(template)
    # running simulations
    simulation.run_all(["name", "balance"], jobs=None)
    # plotting results
    if len(sys.argv) == 1 or sys.argv[1] != "--noplot":
        plot.plot_balance(diff=diff, resolution=resolution)


def grid_search(f, lists, xlabel, ylabel, sorted_count=0):
    # settings
    simulation.global_settings.record_balance = False
    # creating simulations
    simulation.create_grid(lists, f)
    # running simulations
    simulation.run_all(["name", "balance"], jobs=None)
    # printing results
    simulations_copy = simulation.simulations.copy()
    simulations_copy.sort(key=lambda x: x.balance, reverse=True)
    print("==============================================")
    for sim in simulations_copy[:sorted_count]:
        sim.print_props(["name", "balance"])
    open("output.txt", "w")
    file = open("output.txt", "a")
    for sim_i in range(len(simulations_copy)):
        sim = simulations_copy[sim_i]
        file.write(f"<{sim_i + 1}> {sim.get_prop_str(['name', 'balance'])}")
        file.write("\n")
    file.close()
    # plotting results if there are two parameter lists
    plotting_enabled = len(sys.argv) == 1 or sys.argv[1] != "--noplot"
    if plotting_enabled and len(lists) == 2:
        plot.balance_surface_plot(lists[0], lists[1],
                                  xlabel=xlabel, ylabel=ylabel)


if __name__ == "__main__":

    # settings
    simulation.global_settings.precision = 5
    simulation.global_settings.amount = 10**5

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    main_template = {
        "balance": to_curr(100.0),
        "ignore_spread": False,
        "sl_range": 400,
        "tp_range": 100,
        "ma1": 1,
        "ma2": 10,
        "leverage": 500,
        "name": "Untitled"
    }

    # single_sim(main_template)

    # template1 = main_template.copy()
    # template1["name"] = "No closing"
    #
    # template2 = main_template.copy()
    # template2["weekend_closing"] = True
    # template2["name"] = "Closing"
    #
    # sim_list([template1, template2])

    # creating simulations
    def create_sim(ma1, ma2):
        template = main_template.copy()
        template["name"] = f"{ma1} {ma2}"
        template["ma1"] = ma1
        template["ma2"] = ma2
        simulation.add_from_template(template)
    grid_search(
        create_sim,
        [list(range(1, 11)), list(range(1, 11))],
        "ma1", "ma2",
        sorted_count=10
    )
