import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d  # noqa
import numpy as np
import simulation
import utils
import indicators


def plot_balance(diff=None, length=None):
    for sim in simulation.simulations:
        balance_record = simulation.from_curr(sim.balance_record)
        if diff:
            deriv = np.diff(balance_record)
            balance_record = utils.moving_average(deriv, length)
            plt.plot([0, len(balance_record)], [0, 0], color="red")
        plt.plot(balance_record, label=sim.name)
    plt.legend(loc="upper left")
    plt.show()


def plot_orders(plot_indicators):
    for sim in simulation.simulations:
        indicator = list(indicators.indicators.values())[-1]
        if plot_indicators and indicator.requires_subplot():
            plt.subplot(211)
        plt.plot(simulation.from_curr(simulation.global_data.price_data))
        for order in sim.order_record:
            dot_color = None
            if order[2] == simulation.OrderType.BUY:
                dot_color = "green"
            if order[2] == simulation.OrderType.SELL:
                dot_color = "red"
            if order[2] == simulation.OrderType.CLOSE:
                dot_color = "black"
            plt.scatter(order[0], order[1], color=dot_color)
        if plot_indicators:
            indicator.plot()
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
