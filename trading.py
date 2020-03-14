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
        "balance": to_curr(100.0),
        "ignore_spread": False,
        "sl_range": 400,
        "tp_range": 100,
        "ma1": 21,
        "ma2": 32,
        "leverage": 500,
        "name": "Untitled"
    }

    # creating simulations

    # ma1lst = list(range(1, 41))
    # ma2lst = ma1lst[:]
    #
    # def create_sim(ma1, ma2):
    #     template = main_template.copy()
    #     template["name"] = f"{ma1} {ma2}"
    #     template["ma1"] = ma1
    #     template["ma2"] = ma2
    #     simulation.add_from_template(template)
    #
    # simulation.create_grid(ma1lst, ma2lst, create_sim)

    template = main_template.copy()
    simulation.add_from_template(template)

    # running simulations
    simulation.run_all(["name", "balance"])

    # balance plot
    # plot.balance_surface_plot(ma1lst, ma2lst, xlabel="ma1", ylabel="ma2")
    plot.plot_balance()
