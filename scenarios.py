import simulation
import strategies


def startup(skip, amount, filename):
    simulation.init()
    simulation.global_settings.precision = 5
    simulation.global_settings.skip = skip
    simulation.global_settings.amount = amount
    simulation.load_file(filename)


def smallfile(amount):
    skip = 1000000 - amount
    startup(skip, amount, "EURUSD_i_M1_201706131104_202002240839.csv")


def bigfile(amount):
    skip = 7649335 - amount
    startup(skip, amount, "EURUSD_M1_199901041022_202004171116.csv")


def simple_ma(amount):
    bigfile(amount)
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
        "brlen": 10000,
        "name": "Untitled"
    }
    simulation.sim_list([template])
    print()


def balancerec_strat(amount):
    bigfile(amount)
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
        "brlen": 10000,
        "name": "Untitled"
    }
    simulation.sim_list([template])
    print()


def save_balancerec(amount, plot_balance=False):
    bigfile(amount)
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
    simulation.save_mas(template, pairs_list, plot_balance=plot_balance)
    print()


def balancerec_strat_cmp(amount):
    bigfile(amount)
    main_template = {
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
        "brlen": 10000,
        "name": "Untitled"
    }
    brlens = [i * 1000 for i in range(5, 21)]
    templates = []
    for brlen in brlens:
        template = main_template.copy()
        template["brlen"] = brlen
        template["name"] = f"{brlen}"
        templates.append(template)
    simulation.sim_list(templates)
    print()
