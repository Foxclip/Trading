import math
import statistics
import numpy as np


def deriv(lst, batch_count):
    batch_size = math.floor(len(lst) / batch_count)
    print(batch_size)
    deriv_lst = []
    for batch_i in range(batch_count):
        start = batch_i * batch_size
        end = start + batch_size
        if end >= len(lst):
            end = len(lst) - 1
        deriv = (lst[end] - lst[start]) / batch_size
        deriv_lst.append(deriv)
    return deriv_lst


def moving_average(lst, count):
    avg_lst = []
    for i in range(len(lst) - count + 1):
        batch = lst[i:i + count]
        avg = statistics.mean(batch)
        avg_lst.append(avg)
    return avg_lst


def ma(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


lst = []
for i in range(10):
    lst.append(i ** 2)
print(lst)
# print(deriv(lst, 3))
# print(moving_average(lst, 3))
print(ma(lst, 2))
