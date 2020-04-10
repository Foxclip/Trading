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
        "weekend_closing": False,
        "name": "Untitled"
    }
    template_list = []
    pairs_list = [
        [1, 10],
        [9, 10],
        [15, 30],
        [17, 37],
        [4, 8],
    ]
    for pair in pairs_list:
        template = main_template.copy()
        template["ma1"] = pair[0]
        template["ma2"] = pair[1]
        template["name"] = f"{pair[0]} {pair[1]}"
        template_list.append(template)
        template = main_template.copy()
        template["ma1"] = pair[1]
        template["ma2"] = pair[0]
        template["name"] = f"{pair[1]} {pair[0]}"
        template_list.append(template)

    simulation.sim_list(
        template_list,
        diff=True,
        length=10000,
        save_balance=True
    )
    # simulation.grid_search_mas(main_template, 10, 10)
