import numpy as np
from numba.typed import List


def moving_average(lst, length, left_pad=True):
    if length > len(lst):
        raise ValueError("Moving average window length is bigger than list "
                         "length")
    cumsum = np.cumsum(np.insert(lst, 0, 0))
    result = (cumsum[length:] - cumsum[:-length]) / float(length)
    if left_pad:
        missing_values = len(lst) - len(result)
        result = np.pad(result, (missing_values, 0))
    return result


def to_typed_list(lst):
    typed_lst = List()
    [typed_lst.append(x) for x in lst]
    return typed_lst
