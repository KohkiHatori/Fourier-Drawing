# Standard Library
import sys
import os
from math import e
from math import pi
from time import time
from random import choice

# Third Party
from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# My Modules
from coeff import Coefficient_calculator
from svg import SVG
from utils import *
from config import Config
from bezier import PolyBezier
from merge import Merger


class ComplexVector:

    def __init__(self, coefficient: complex, n: int):
        self.coefficient = coefficient
        self.n = n

    def func(self, t) -> float:
        return self.coefficient * (e ** (self.n * 2 * pi * 1j * t))

    def __repr__(self) -> str:
        pass


def sum_comp_vec(vectors, t) -> int | float:
    sum_vec = 0
    for vector in vectors:
        sum_vec += vector.func(t)
    return sum_vec


def animate(sets, xlim, ylim, output=False, show_vectors=True):
    plt.style.use(Config.STYLE)
    fig = plt.figure(figsize=Config.FIG_SIZE)
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    ax = plt.axes(xlim=(xlim[0] - x_range / Config.MARGIN_FACTOR, xlim[1] + x_range / Config.MARGIN_FACTOR),
                  ylim=(ylim[0] - y_range / Config.MARGIN_FACTOR, ylim[1] + y_range / Config.MARGIN_FACTOR))
    plt.gca().set_aspect('equal', adjustable='box')
    ax.axis(Config.AXIS)
    lines = [plt.plot([], [], lw=Config.PATH_WIDTH, color=choice(Config.PATH_COLOURS))[0] for _ in range(len(sets))]
    if show_vectors:
        sets_of_vecs = [[plt.plot([], [], linewidth=Config.VEC_WIDTH)[0] for _ in range(len(compVectors))] for compVectors in
                        sets]
    xdatas = [[] for _ in range(len(sets))]
    ydatas = [[] for _ in range(len(sets))]
    def update(i):
        t = i * (1 / Config.NUM_FRAME)
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
                    x += vector.func(t).real
                    y += vector.func(t).imag
                xdata.append(x)
                ydata.append(y)
                line.set_data(xdata, ydata)
            return *lines,
    ani = animation.FuncAnimation(fig, update, frames=Config.NUM_FRAME, interval=1, repeat=True, blit=True)
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
    compVectors = []
    for step in steps:
        key = list(coefficients.keys())[step]
        coeff = coefficients[key]
        coeff = complex(coeff[0], coeff[1])
        compVector = ComplexVector(coeff, key)
        compVectors.append(compVector)
    return compVectors

def convert_to_svg(file_path: str) -> str:
    filename = get_filename(file_path)
    pnm = f"{filename}.pnm"
    os.system(f"convert {file_path} -background white -alpha remove -alpha off {pnm}")
    filename = get_filename(file_path)
    svg = f"{filename}.svg"
    os.system(f"potrace --flat {pnm} -s -o {svg}")
    os.remove(pnm)
    return svg


def compile_polybeziers(paths: list) -> list:
    polys = []
    for path in paths:
        poly = PolyBezier(path)
        polys.append(poly)
    return polys


def get_sets_coeffs(polys: list, num: int, by_dist: bool = False) -> list:
    sets_of_coeffs = []
    for poly in polys:
        calc = Coefficient_calculator(poly, num, by_dist)
        sets_of_coeffs.append(calc.main())
    return sets_of_coeffs


def get_sets_compVec(sets_of_coeffs: list) -> list:
    sets_of_compVecs = []
    for coeffs in sets_of_coeffs:
        sets_of_compVecs.append(create_compVectors(coeffs))
    return sets_of_compVecs


def get_lims(polys: list):
    lims = [poly.get_lims() for poly in polys]
    xs = [lim[0] for lim in lims]
    ys = [lim[1] for lim in lims]
    xlim = (min(xs, key=lambda item: item[0])[0], max(xs, key=lambda item: item[1])[1])
    ylim = (min(ys, key=lambda item: item[0])[0], max(ys, key=lambda item: item[1])[1])
    return xlim, ylim


def main(file_path, output=False, num_set=0):
    initial = time()
    # Convert to svg
    if get_extension(file_path) != "svg":
        file_path = convert_to_svg(file_path)
    # Get polybezier from the svg file
    data = get_file_content(file_path)

    paths = SVG(data).parse_path()
    #paths = Merger(paths, num_set).main()
    polybeziers = compile_polybeziers(paths)
    sets_of_coeffs = get_sets_coeffs(polybeziers, Config.NUM_VECTORS, Config.BY_DIST)
    # Create compVector objects


    sets_of_compVectors = get_sets_compVec(sets_of_coeffs)
    final = time()
    print(f"Time taken: {final - initial}")
    show_vectors = len(paths) < Config.VEC_DISPLAY_THRESHOLD
    animate(sets_of_compVectors, *get_lims(polybeziers), output=output, show_vectors=show_vectors)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main("/Users/kohkihatori/NEA/API/example_pictures/mona lisa.jpeg")
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
