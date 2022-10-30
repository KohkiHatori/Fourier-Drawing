import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from function import Function
from svg import SVG
from bezier import *
import sys
import os
from math import e
from math import pi
import math
import numpy as np



class ComplexVector:

    def __init__(self, coefficient, n):
        self.coefficient = coefficient
        self.n = n

    def func(self, t) -> float:
        return self.coefficient * (e ** (self.n * 2 * pi * 1j * t))

    def __repr__(self) -> str:
        pass


def sum_comp_vec(vectors, t) -> int | float:
    sum = 0
    for vector in vectors:
        sum += vector.func(t)
    return sum


def create_vec_data(compVectors, t):
    data = []
    for vector in compVectors:
        data.append([vector.func(t).real, vector.func(t).imag])
    data = np.array(data)
    origin = np.insert(data, 0, [0, 0], axis=0)
    origin = np.delete(origin, -1, axis=0)
    origin = origin.transpose()
    origin = origin.cumsum(axis=1)
    return data, origin

def animate(compVectors, xlim, ylim, output=False):
    # number of frames.
    num = 1000
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(19,10))
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    ax = plt.axes(xlim=(xlim[0]-x_range/7, xlim[1]+x_range/7), ylim=(ylim[0]-y_range/7, ylim[1]+y_range/7))
    plt.gca().set_aspect('equal', adjustable='box')
    xdata = []
    ydata = []
    line, = plt.plot([], [], lw=2)
    colors = []
    vecs = [plt.plot([], [], linewidth=0.5)[0] for _ in range(len(compVectors))]
    def update(i):
        t = i*(1/num)
        x = 0
        y = 0
        for vector, plot in zip(compVectors, vecs):
            x_updated = x + vector.func(t).real
            y_updated = y + vector.func(t).imag
            plot.set_data([x, x_updated], [y, y_updated])
            x = x_updated
            y = y_updated
        xdata.append(x)
        ydata.append(y)
        line.set_data(xdata, ydata)
        return line, *vecs
    ani = animation.FuncAnimation(fig, update, frames=num, interval=1, repeat=True, blit=True)
    if output:
        writervideo = animation.FFMpegWriter(fps=60)
        ani.save('test.mp4', writer=writervideo)
    plt.show()

def frame(compVectors, t):
    #plt.style.use('dark_background')
    fig = plt.figure()
    ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
    plt.gca().set_aspect('equal', adjustable='box')
    centre = np.array([0.0, 0.0])
    for vector in compVectors:
        circle = plt.Circle(tuple(centre), abs(vector.func(t)), fill=False)
        ax.add_patch(circle)
        centre += np.array([vector.func(t).real, vector.func(t).imag])
    data, origin = create_vec_data(compVectors, t)
    plt.quiver(*origin, data[:, 0], data[:, 1], scale=1, scale_units="xy", color="blue")
    plt.show()


def create_compVectors(coefficients):
    index = len(coefficients)//2 - (len(coefficients) % 2 == 0)
    steps = []
    for i in range(len(coefficients)):
        steps.append(index)
        index += (-1) ** (i % 2 != 0) * (i + 1)
    compVectors = [ComplexVector(coefficients[list(coefficients.keys())[i]], list(coefficients.keys())[i]) for i in steps]
    return compVectors


def potrace(pnm_path):
    filename = get_filename(file_path)
    svg = f"{filename}.svg"
    os.system(f"potrace --flat {pnm_path} -s -o {svg}")
    return f"{get_filename(pnm_path)}.svg"


def convert_to_pnm(file_path):
    filename = get_filename(file_path)
    pnm = f"{filename}.pnm"
    os.system(f"convert {file_path} {pnm}")
    return pnm


def delete_pnm(file_path):
    os.remove(file_path)


def convert_to_svg(file_path):
    pnm = convert_to_pnm(file_path)
    svg = potrace(pnm)
    delete_pnm(pnm)
    return svg


def main(file_path, output=False):
    # Convert to svg
    if get_extension(file_path) != "svg":
        file_path = convert_to_svg(file_path)
    # Get polybezier from the svg file
    file = get_file_content(file_path)
    tes = SVG(file)
    poly = PolyBezier(tes.parse_path())
    # Get coefficients from the polybezier
    func = Function(poly.func)
    coeffs = func.get_coefficients()
    # Create compVector objects
    compVectors = create_compVectors(coeffs)
    animate(compVectors, func.xlim, func.ylim, output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python test_display.py "image file name" ')
    else:
        file_name = sys.argv[1]
        if file_name == "sample":
            file_path = os.path.abspath("example_pictures/pi.svg")
        else:
            file_path = os.path.abspath(file_name)
        if len(sys.argv) >= 3:
            main(file_path, sys.argv[2] == "output")
        else:
            main(file_path)