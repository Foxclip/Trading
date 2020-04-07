import simulation
from simulation import to_curr
import strategies


if __name__ == "__main__":

    simulation.init()

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
        "macd_s": 12,
        "macd_l": 26,
        "macd_t": 9,
        "leverage": 500,
        "direction": simulation.Direction.REVERSE,
        "strategy": strategies.moving_averages,
        "name": "Untitled"
    }

    # simulation.sim_list([main_template], diff=True)
    simulation.grid_search_mas(main_template, 10, 10)
