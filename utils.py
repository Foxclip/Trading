import numpy as np
from numba.typed import List


def moving_average(lst, length, left_pad=True):
    cumsum = np.cumsum(np.insert(lst, 0, 0))
    result = (cumsum[length:] - cumsum[:-length]) / float(length)
    if left_pad:
        missing_values = len(lst) - len(result)
        result = np.pad(result, (missing_values, 0))
    return result


def copydict(d, manager_d):
    for key in d.keys():
        manager_d[key] = d[key]


def copylist(l, manager_l):
    for v in l:
        manager_l.append(v)


def to_typed_list(lst):
    typed_lst = List()
    [typed_lst.append(x) for x in lst]
    return typed_lst
