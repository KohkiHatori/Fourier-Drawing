from utils import *
import numpy as np


class Bezier:

    degree = {
        2: "Linear",
        3: "Quadratic",
        4: "Cubic",
        5: "Quartic",
        6: "Quintic"
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

    def derived(self, t: float):
        length = len(self.points)
        if length == 4:
            point = self.cubic(t)
        elif length == 2:
            point = lerp(self.points[0], self.points[1], t)
        else:
            raise Exception
        return point

    def cubic(self, t: float):
        return (1-t)**3 * self.points[0] + 3 * (1-t)**2 * t * self.points[1] + 3 * (1-t) * t**2 * self.points[2] + t**3 * self.points[3]

    def get_lims(self):
        pass

    def __repr__(self) -> str:
        out = f"{self.degree[len(self.points)]} Bezier Curve: "
        for index, point in enumerate(self.points):
            out += f"Point{index+1}: ({point.real}, {point.imag}) "
        return out

class CubicBezier(Bezier):

    pass

class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        self.num = len(self.beziers)

    def func(self, t: float) -> complex:
        index = int(t // (1 / self.num))
        if index == self.num:
            bez = self.beziers[index-1]
        else:
            bez = self.beziers[index]
        #return bez.de_Casteljau(bez.points, t * self.num - index)
        return bez.derived(t * self.num - index)

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
