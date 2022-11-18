# Standard Library
import sys
import os
from math import e
from math import pi
from time import time

from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from coeff import Coefficient_calculator
from svg import SVG
from bezier import *
from config import *


# def frame(compVectors, t):
#     #plt.style.use('dark_background')
#     fig = plt.figure()
#     ax = plt.axes(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
#     plt.gca().set_aspect('equal', adjustable='box')
#     centre = np.array([0.0, 0.0])
#     for vector in compVectors:
#         circle = plt.Circle(tuple(centre), abs(vector.func(t)), fill=False)
#         ax.add_patch(circle)
#         centre += np.array([vector.func(t).real, vector.func(t).imag])
#     data, origin = create_vec_data(compVectors, t)
#     plt.quiver(*origin, data[:, 0], data[:, 1], scale=1, scale_units="xy", color="blue")
#     plt.show()
#
# def create_vec_data(compVectors, t):
#     data = []
#     for vector in compVectors:
#         data.append([vector.func(t).real, vector.func(t).imag])
#     data = np.array(data)
#     origin = np.insert(data, 0, [0, 0], axis=0)
#     origin = np.delete(origin, -1, axis=0)
#     origin = origin.transpose()
#     origin = origin.cumsum(axis=1)
#     return data, origin


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


def animate(sets, xlim, ylim, output=False, show_vectors=True, axis_off=True):
    # number of frames.
    plt.style.use(STYLE)
    fig = plt.figure(figsize=FIG_SIZE)
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    ax = plt.axes(xlim=(xlim[0] - x_range / MARGIN, xlim[1] + x_range / MARGIN),
                  ylim=(ylim[0] - y_range / MARGIN, ylim[1] + y_range / MARGIN))
    plt.gca().set_aspect('equal', adjustable='box')
    if axis_off:
        ax.axis("off")
    lines = [plt.plot([], [], lw=PATH_WIDTH, color=PATH_COLOR)[0] for _ in range(len(sets))]
    if show_vectors:
        sets_of_vecs = [[plt.plot([], [], linewidth=VEC_WIDTH)[0] for _ in range(len(compVectors))] for compVectors in
                        sets]
    xdatas = [[] for _ in range(len(sets))]
    ydatas = [[] for _ in range(len(sets))]
    def update(i):
        t = i * (1 / NUM_FRAME)
        if show_vectors:
            for compVectors, line, vecs, xdata, ydata in zip(sets, lines, sets_of_vecs, xdatas, ydatas):
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
            return *lines, *chain.from_iterable(sets_of_vecs)
        else:
            for compVectors, line, xdata, ydata in zip(sets, lines, xdatas, ydatas):
                x = 0
                y = 0
                for vector in compVectors:
                    x_updated = x + vector.func(t).real
                    y_updated = y + vector.func(t).imag
                    x = x_updated
                    y = y_updated
                xdata.append(x)
                ydata.append(y)
                line.set_data(xdata, ydata)
            return *lines,
    ani = animation.FuncAnimation(fig, update, frames=NUM_FRAME, interval=1, repeat=True, blit=True)
    if output:
        writervideo = animation.FFMpegWriter(fps=60)
        ani.save('test.mp4', writer=writervideo)
    plt.show()


def create_compVectors(coefficients):
    index = len(coefficients) // 2 - (len(coefficients) % 2 == 0)
    steps = []
    for i in range(len(coefficients)):
        steps.append(index)
        index += (-1) ** (i % 2 != 0) * (i + 1)
    compVectors = [ComplexVector(coefficients[list(coefficients.keys())[i]], list(coefficients.keys())[i]) for i in
                   steps]
    return compVectors


def potrace(pnm_path: str) -> str:
    filename = get_filename(file_path)
    svg = f"{filename}.svg"
    os.system(f"potrace --flat {pnm_path} -s -o {svg}")
    return f"{get_filename(pnm_path)}.svg"


def convert_to_pnm(file_path: str) -> str:
    filename = get_filename(file_path)
    pnm = f"{filename}.pnm"
    os.system(f"convert {file_path} -background white -alpha remove -alpha off {pnm}")
    return pnm


def delete_pnm(file_path: str):
    os.remove(file_path)


def convert_to_svg(file_path: str) -> str:
    pnm = convert_to_pnm(file_path)
    svg = potrace(pnm)
    delete_pnm(pnm)
    return svg


def create_polybeziers(paths: list) -> list:
    polys = []
    for path in paths:
        poly = PolyBezier(path)
        polys.append(poly)
    return polys


def get_sets_coeffs(polys: list, num: int) -> list:
    sets_of_coeffs = []
    for poly in polys:
        calc = Coefficient_calculator(poly, num)
        sets_of_coeffs.append(calc.main())
        # func = Function(poly.func)
        # sets_of_coeffs.append(func.get_coefficients())
    return sets_of_coeffs


def get_sets_compVec(sets_of_coeffs: list) -> list:
    sets_of_compVecs = []
    for coeffs in sets_of_coeffs:
        sets_of_compVecs.append(create_compVectors(coeffs))
    return sets_of_compVecs


def get_lims(polys: list):
    lims = {lim[0]: lim[1] for lim in [poly.get_lims() for poly in polys]}
    xs = list(lims.keys())
    ys = list(lims.values())
    xlim = (min(xs, key=lambda item: item[0])[0], max(xs, key=lambda item: item[1])[1])
    ylim = (min(ys, key=lambda item: item[0])[0], max(ys, key=lambda item: item[1])[1])
    return xlim, ylim


def main(file_path, output=False, num_set=0):
    initial = time()
    # Convert to svg
    if get_extension(file_path) != "svg":
        file_path = convert_to_svg(file_path)
    # Get polybezier from the svg file
    file = get_file_content(file_path)

    paths = SVG(file).parse_path()
    #paths = merge(paths, num_set)
    polybeziers = create_polybeziers(paths)
    sets_of_coeffs = get_sets_coeffs(polybeziers, NUM_VECTORS)
    # Create compVector objects
    sets_of_compVectors = get_sets_compVec(sets_of_coeffs)
    final = time()
    print(f"Time taken: {final - initial}")
    show_vectors = len(paths) < VEC_DISPLAY_THRESHOLD
    animate(sets_of_compVectors, *get_lims(polybeziers), output=output, show_vectors=show_vectors, axis_off=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main("/Users/kohkihatori/NEA/API/example_pictures/pi.svg")
        # print('Usage: python test_display.py "image file name" ')
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
