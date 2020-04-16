import simulation
import strategies


def startup(amount):
    simulation.init()
    simulation.global_settings.precision = 5
    simulation.global_settings.amount = amount
    simulation.load_file("EURUSD_i_M1_201706131104_202002240839.csv")


def balancerec_strat(amount):
    startup(amount)
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


def save_balancerec(amount):
    startup(amount)
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


def balancerec_strat_cmp(amount):
    startup(amount)
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
