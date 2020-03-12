import numpy as np


def moving_average(lst, length, left_pad=True):
    cumsum = np.cumsum(np.insert(lst, 0, 0))
    result = (cumsum[length:] - cumsum[:-length]) / float(length)
    if left_pad:
        missing_values = len(lst) - len(result)
        result = np.pad(result, (missing_values, 0))
    return result
