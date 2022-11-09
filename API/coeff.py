from math import pi, e
import numpy as np


class Coefficient_calculator:

    def __init__(self, poly_bezier, num):
        self.poly_bezier = poly_bezier
        self.num = num

    def get_coefficient(self, n):
        integrals = []
        denom = -n * 2 * pi * 1j
        num = len(self.poly_bezier)
        for index, bezier in enumerate(self.poly_bezier.beziers):
            upper = e ** (denom * index+1)
            lower = e ** (denom * index)
            if len(bezier.points) == 4:
                a = -bezier.points[0] + 3 * bezier.points[1] - 3 * bezier.points[2] + bezier.points[3]
                b = 3 * bezier.points[0] - 6 * bezier.points[1] + 3 * bezier.points[2]
                c = -3 * bezier.points[0] + 3 * bezier.points[1]
                d = bezier.points[0]
                if n == 0:
                    result = a / 4 + b / 3 + c / 2 + d
                else:
                    first = ((a+b+c+d)*upper-d*lower)/denom
                    second = - ((3*a+2*b+c)*upper-c*lower)/(denom**2)
                    third = ((6*a+2*b)*upper-2*b*lower)/(denom**3)
                    fourth = - (6*a*(upper-lower))/(denom**4)
                    result = first + second + third + fourth
            elif len(bezier.points) == 2:
                zero = bezier.points[0]
                one = bezier.points[1]
                if n == 0:
                    result = zero + (one - zero) / 2
                else:
                    result = ((one*upper-zero*lower)/denom) - ((one-zero)*(upper+lower)/(denom**2))
            else:
                raise SyntaxError("Only cubic and linear bezier curves are supported.")
            integrals.append(result)
        return sum(integrals)

    def main(self):
        start = -round(self.num/2 - 1)
        # The middle value of frequency should be 0, so the minimum frequency is "start"
        # e.g. If the NUM is 10, the minimum frequency is -4.
        coeffs = []
        steps = np.arange(start, start + self.num)
        for n in steps:
            coeffs.append(self.get_coefficient(n))
        return dict(zip(steps, coeffs))
