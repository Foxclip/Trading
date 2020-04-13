import simulation
import strategies

moving_averages = {
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

balance_records = {
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
