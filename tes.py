"""
Date created: 6 July 2022
Author: Kohki Hatori 
Description: 
    This program visualises fourier transform graphs.
    The idea is based on this video: 
    https://www.youtube.com/watch?v=spUNpyF58BY&list=PLCNiBhi0_aBHX-trdOXAIk_q6SBaHgWlo&index=11
"""
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

PI = math.pi
LOWER = 0
UPPER = 5
SAMPLE_FREQUENCY = 0.0001
CYCLE_RANGE = 10000
"""
limits and step to go through the original function
"""


def get_mags(function, cycle_freqs):
    mags = []
    argand_xs_hist = []
    argand_ys_hist = []
    com_xs = []
    com_ys = []
    for cycle_freq in cycle_freqs:
        argand_xs, argand_ys, centre_of_mass_x, centre_of_mass_y = get_com(function, cycle_freq)
        argand_xs_hist.append(argand_xs)
        argand_ys_hist.append(argand_ys)
        com_xs.append(centre_of_mass_x)
        com_ys.append(centre_of_mass_y)
        mag = get_magnitude(centre_of_mass_x, centre_of_mass_y)
        mags.append(mag)
    plot_com(argand_xs_hist, argand_ys_hist, com_xs, com_ys)
    return np.array(mags)

def get_com(function, cycle_freq):
    """
    Get the "centre of mass" of the function that's been winded around a circle.
    """
    xs = np.linspace(LOWER, UPPER, int(1/SAMPLE_FREQUENCY))
    thetas = get_thetas(xs, cycle_freq)
    r = function(xs)
    argand_xs = r*np.cos(thetas)
    argand_ys = r*np.sin(thetas)
    centre_of_mass_x = np.mean(argand_xs)
    centre_of_mass_y = np.mean(argand_ys)
    return argand_xs, argand_ys, centre_of_mass_x, centre_of_mass_y

def get_thetas(xs, cycle_freq):
    if cycle_freq != 0.0:
        return PI * 2 * xs * cycle_freq
    else:
        return 0

def my_func(xs):
    return np.cos(9*PI*xs) + np.cos(6 * PI * xs) + np.cos(3 * PI * xs)

def get_magnitude(x, y):
    return math.sqrt(x ** 2 + y ** 2)

def plot_com(argand_xs_hist, argand_ys_hist, com_xs, com_ys):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    plot0 = ax.plot(argand_xs_hist[0], argand_ys_hist[0], linewidth=1, color="red")
    plot1 = ax.plot(com_xs[0], com_ys[0], 'ro')
    plt.subplots_adjust(bottom=0.05, left=0.05)
    lim = 1.4
    ax.set(xlim=(-lim, lim), xticks=np.arange(-lim, lim),
          ylim=(-lim, lim), yticks=np.arange(-lim, lim, 5))
    def update(i):
        new_argand_xs = argand_xs_hist[i]
        new_argand_ys = argand_ys_hist[i]
        plot0[0].set_xdata(new_argand_xs)
        plot0[0].set_ydata(new_argand_ys)
        plot1[0].set_xdata(com_xs[i])
        plot1[0].set_ydata(com_ys[i])
        return plot0, plot0
    anim = FuncAnimation(fig, update, frames=range(CYCLE_RANGE), interval=CYCLE_RANGE*0.0005, repeat=True)
    plt.show()



x = np.linspace(0, 4, CYCLE_RANGE)
# range and step of cycle frequency
y = get_mags(my_func, x)

plt.style.use("_mpl-gallery")
fig, ax = plt.subplots(figsize=(10,10))
plt.subplots_adjust(bottom=0.05, left=0.05)

ax.plot(x, y, linewidth=1, color="red")
xlim = 10
ylim = 0.5
# ax.set(xlim=(0, xlim), xticks=np.arange(1, xlim),
#      ylim=(-ylim, ylim), yticks=np.arange(-ylim, ylim, 5))

plt.show()
