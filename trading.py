import matplotlib.pyplot as plt
import simulation
from simulation import to_curr, from_curr


if __name__ == "__main__":

    # settings
    simulation.precision = 5
    simulation.amount = 10000

    # loading file
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")

    # creating simulations
    main_template = {
        "balance": to_curr(1000, simulation.precision),
        "ma_length": 15,
        "ignore_spread": False,
        "put_stops": True,
        "sl_range": 100,
        "tp_range": 500,
        "name": "Untitled"
    }
    template = main_template.copy()
    template["tp_range"] = 400
    template["name"] = "400"
    simulation.add_from_template(template)
    template = main_template.copy()
    template["tp_range"] = 500
    template["name"] = "500"
    simulation.add_from_template(template)
    template = main_template.copy()
    template["tp_range"] = 600
    template["name"] = "600"
    simulation.add_from_template(template)

    # running simulations
    simulation.run_all()

    # plotting results
    for sim in simulation.simulations:
        record = sim.balance_record
        precision = simulation.precision
        balance_record1 = from_curr(record, precision)
        plt.plot(balance_record1, label=sim.name)
    plt.legend(loc="upper right")
    plt.show()
