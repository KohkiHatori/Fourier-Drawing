from utils import *
import numpy as np


class Bezier:

    degree = {
        1: "Linear",
        2: "Quadratic",
        3: "Cubic",
        4: "Quartic",
        5: "Quintic"
    }

    def __init__(self, points: list):
        self.points = points

    def de_Casteljau(self, points: list, t: float):
        if len(points) == 1:
            in_complex_form = complex(points[0][0], points[0][1])
            return in_complex_form
        else:
            new_points = []
            for i in range(len(points) - 1):
                new_points.append(lerp(points[i], points[i + 1], t))
            return self.de_Casteljau(new_points, t)

    def derived(self, points: list, t: float):
        length = len(points)
        if length == 4:
            point = self.cubic(points, t)
        elif length == 3:
            point = self.quadratic(points, t)
        elif length == 2:
            point = lerp(points[0], points[1], t)
        else:
            raise Exception
        return point

    def cubic(self, points: list, t: float):
        return (1-t)**3 * points[0] + 3 * (1-t)**2 * t * points[1] + 3 * (1-t) * t**2 * points[2] + t**3 * points[3]

    def quadratic(self, points: list, t: float):
        return (1-t) ** 2 * points[0] + 2 * (1-t) * t * points[1] + t**2 * points[2]

    def get_lims(self):
        pass

    def __repr__(self) -> str:
        out = f"{self.degree[len(self.points)]} Bezier Curve: "
        for index, point in enumerate(self.points):
            out += f"Point{index+1}: ({point[0]}, {point[1]}) "
        return out


class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        self.num = len(self.beziers)

    def func(self, t: float) -> complex:
        index = int(t // (1 / self.num))
        if index == self.num:
            index -= 1
        bez = self.beziers[index]
        #return bez.de_Casteljau(bez.points, t * self.num - index)
        return bez.derived(bez.points, t * self.num - index)

    def get_lims(self):
        """
        :return: The maximum and minimum values of real and imaginary values.
        """
        dt = 0.001
        value_dict = {t: self.func(t) for t in np.arange(0, 1+dt, dt)}
        vals = value_dict.values()
        real = [val.real for val in vals]
        imag = [val.imag for val in vals]
        xlim = (min(real), max(real))
        ylim = (min(imag), max(imag))
        return xlim, ylim

    def __repr__(self) -> str:
        return f"PolyBezier object consisting of {self.num} bezier curves"

    def __len__(self) -> int:
        return self.num
