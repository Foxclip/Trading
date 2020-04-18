import simulation
import strategies

main = {
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

ma = main.copy()

balancerec = main.copy()
balancerec["strategy"] = strategies.balance_records

balancetime = main.copy()
balancetime["strategy"] = strategies.balancetime
