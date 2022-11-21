from math import pi, e
import numpy as np


class Coefficient_calculator:

    def __init__(self, poly_bezier, num):
        self.poly_bezier = poly_bezier
        self.num_coeff = num
        self.num_bez = len(self.poly_bezier)

    def get_coefficient(self, n: int):
        integrals = []
        self.denom = -n * 2 * pi * 1j
        lower = 0
        upper = 0
        for index, bezier in enumerate(self.poly_bezier.beziers):
            upper += bezier.dist/self.poly_bezier.dist
            self.upper_e = e ** (self.denom * upper)
            self.lower_e = e ** (self.denom * lower)
            if bezier.degree == 3:
                result = self._get_integral_cubic(bezier, n)
            elif bezier.degree == 1:
                result = self._get_integral_linear(bezier, n)
            else:
                raise SyntaxError("Only cubic and linear bezier curves are supported.")
            integrals.append(result)
            lower = upper
        return sum(integrals)

    def _get_integral_cubic(self, bezier, n: int) -> complex:
        a = -bezier.p(0) + 3 * bezier.p(1) - 3 * bezier.p(2) + bezier.p(3)
        b = 3 * bezier.p(0) - 6 * bezier.p(1) + 3 * bezier.p(2)
        c = -3 * bezier.p(0) + 3 * bezier.p(1)
        d = bezier.p(0)
        dudt = self.poly_bezier.dist/bezier.dist
        if n == 0:
            result = (a / 4 + b / 3 + c / 2 + d) / dudt
        else:
            first = ((a + b + c + d) * self.upper_e - d * self.lower_e) / self.denom
            second = -(dudt * ((3 * a + 2 * b + c) * self.upper_e - c * self.lower_e) / (self.denom ** 2))
            third = (dudt ** 2 * ((6 * a + 2 * b) * self.upper_e - 2 * b * self.lower_e)) / (self.denom ** 3)
            fourth = -((dudt ** 3 * 6*a * (self.upper_e - self.lower_e)) / (self.denom ** 4))
            result = first + second + third + fourth
        return result

    def _get_integral_linear(self, bezier, n: int) -> complex:
        zero = bezier.p(0)
        one = bezier.p(1)
        dudt = self.poly_bezier.dist/bezier.dist
        if n == 0:
            result = ((zero + (one - zero) / 2) / dudt)
        else:
            result = ((one * self.upper_e - zero * self.lower_e) / self.denom) - (dudt * (one - zero) * (
                    self.upper_e - self.lower_e) / (self.denom ** 2))
        return result

    def main(self) -> dict:
        start = -round(self.num_coeff / 2 - 1)
        # The middle value of frequency should be 0, so the minimum frequency is "start"
        # e.g. If the NUM is 10, the minimum frequency is -4.
        coeffs = []
        steps = np.arange(start, start + self.num_coeff)
        for n in steps:
            coeffs.append(self.get_coefficient(n))
        return dict(zip(steps, coeffs))
