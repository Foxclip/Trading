import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d  # noqa
import numpy as np
import simulation
import utils


def simple_deriv(lst):
    deriv_lst = []
    for i in range(len(lst) - 1):
        deriv_lst.append(lst[i + 1] - lst[i])
    return deriv_lst


def plot_balance(diff=False, resolution=10):
    for sim in simulation.simulations:
        balance_record = simulation.from_curr(sim.balance_record)
        if diff:
            count = simulation.amount // resolution
            deriv = simple_deriv(balance_record)
            balance_record = utils.moving_average(deriv, count)
            plt.plot([0, len(balance_record)], [0, 0], color="red")
        plt.plot(balance_record, label=sim.name)
    plt.legend(loc="upper left")
    plt.show()


def plot_orders():
    for sim in simulation.simulations:
        plt.plot(simulation.from_curr(simulation.global_data.price_data))
        for order in sim.order_record:
            type_buy = order[2] == simulation.OrderType.BUY
            dot_color = "green" if type_buy else "red"
            plt.scatter(order[0], order[1], color=dot_color)
        plt.show()


def surface_plot(x, y, z, xlabel="", ylabel=""):
    x, y = np.meshgrid(x, y)
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.plot_surface(x, y, z, cmap='plasma')
    plt.show()


def balance_surface_plot(x, y, xlabel, ylabel):
    x = np.array(x[:])
    y = np.array(y[:])
    balance_arr = np.array([simulation.from_curr(sim.balance)
                            for sim
                            in simulation.simulations])
    z = balance_arr.reshape(len(y), len(x))
    surface_plot(x, y, z, xlabel=xlabel, ylabel=ylabel)
