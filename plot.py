import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d  # noqa
import numpy as np
import simulation
from simulation import from_curr


def plot_balance():
    for sim in simulation.simulations:
        record = sim.balance_record
        precision = simulation.precision
        balance_record = from_curr(record, precision)
        plt.plot(balance_record, label=sim.name)
    plt.legend(loc="upper left")
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
    balance_arr = np.array([from_curr(sim.balance, simulation.precision)
                            for sim
                            in simulation.simulations])
    z = balance_arr.reshape(len(y), len(x))
    surface_plot(x, y, z, xlabel="SL", ylabel="TP")
