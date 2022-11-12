from utils import *


class Bezier:

    degrees = {
        1: "Linear",
        2: "Quadratic",
        3: "Cubic",
        4: "Quartic",
        5: "Quintic",
    }

    def __init__(self, points):
        self.degree = None
        self.points = points

    def p(self, i: int):
        return self.points[i]

    def __repr__(self) -> str:
        out = f"{self.degrees[self.degree]} Bezier Curve: "
        for index, point in enumerate(self.points):
            out += f"Point{index + 1}: ({point.real}, {point.imag}) "
        return out


class CubicBezier(Bezier):

    def __init__(self, points):
        super().__init__(points)
        self.degree = 3

    def func(self, t: float):
        return (1 - t) ** 3 * self.p(0) + 3 * (1 - t) ** 2 * t * self.p(1) + 3 * (1 - t) * t ** 2 * self.p(2) + t ** 3 * self.p(3)

    def get_lims(self):
        possible_maxima_minima = [self.p(0), self.p(1), *self._get_solutions_to_derivatives()]
        coordinates = {point.real: point.imag for point in possible_maxima_minima}
        xs = list(coordinates.keys())
        ys = list(coordinates.values())
        xlim = (min(xs), max(xs))
        ylim = (min(ys), max(ys))
        return xlim, ylim

    def _get_solutions_to_derivatives(self):
        a = -3*self.p(0) + 9*self.p(1) - 9*self.p(2) + 3*self.p(3)
        b = 6*self.p(0) + -12*self.p(1) + 6*self.p(2)
        c = -3*self.p(0) + 3*self.p(1)
        tx1, tx2 = quadratic(a.real, b.real, c.real)
        ty1, ty2 = quadratic(a.imag, b.imag, c.imag)
        ts = [tx1, tx2, ty1, ty2]
        solutions = []
        for t in ts:
            if t is not None and 0 <= t <= 1:
                solutions.append(self.func(t))
        return solutions


class LinearBezier(Bezier):

    def __init__(self, points):
        super().__init__(points)
        self.degree = 1

    def func(self, t: float):
        return lerp(self.p(0), self.p(1), t)

    def get_lims(self):
        possible_maxima_minima = [self.p(0), self.p(1)]
        coordinates = {point.real: point.imag for point in possible_maxima_minima}
        xs = list(coordinates.keys())
        ys = list(coordinates.values())
        xlim = (min(xs), max(xs))
        ylim = (min(ys), max(ys))
        return xlim, ylim


class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        self.num = len(self.beziers)

    def get_lims(self):
        """
        :return: The maximum and minimum values of real and imaginary values.
        """
        lims = {lim[0]: lim[1] for lim in [bez.get_lims() for bez in self.beziers]}
        xs = list(lims.keys())
        ys = list(lims.values())
        xlim = (min(xs, key=lambda item: item[0])[0], max(xs, key=lambda item: item[1])[1])
        ylim = (min(ys, key=lambda item: item[0])[0], max(ys, key=lambda item: item[1])[1])
        return xlim, ylim

    def __repr__(self) -> str:
        return f"PolyBezier object consisting of {self.num} bezier curves"

    def __len__(self) -> int:
        return self.num
