import simulation
import strategies


def startup():
    simulation.init()
    simulation.global_settings.precision = 5
    simulation.global_settings.amount = 10**5
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")


def balancerec_strat():
    startup()
    template = {
        "balance": simulation.to_curr(100.0),
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
        "strategy": strategies.balance_records,
        "weekend_closing": False,
        "name": "Untitled"
    }
    simulation.sim_list([template])
    print()


def save_balancerec():
    startup()
    template = {
        "balance": simulation.to_curr(100.0),
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
    pairs_list = [
        [1, 10],
        [9, 10],
        [15, 30],
        [17, 37],
        [4, 8],
    ]
    simulation.save_mas(template, pairs_list)
    print()
