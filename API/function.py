from math import e
from math import pi
import numpy as np


class Function:
    """

    """

    # The step of t. t goes from 0 to 1, so the number of steps is the reciprocal of DT.
    DT = 0.0001
    # The number of rotating vectors used in the drawing
    NUM = 100

    def __init__(self, function):
        self.func = function

    def get_coefficient(self, n):
        """
        This function calculates the coefficient for a rotating vector with a frequency of n
        :param n: The frequency of the rotaing vector
        :return: The coefficient
        """
        steps = np.arange(0, 1 + self.DT, self.DT)
        coefficient = sum(self.shifted_func(self, n, steps))
        return coefficient

    def get_coefficients(self):
        """
        This function gets a coefficient for each vector.
        :return: A dictionary with keys "steps" and values "coeffs"
        """
        start = -round(self.NUM/2 - 1)
        # The middle value of frequency should be 0, so the minimum frequency is "start"
        # e.g. If the NUM is 10, the minimum frequency is -4.
        coeffs = []
        steps = np.arange(start, start + self.NUM)
        for n in steps:
            coeffs.append(self.get_coefficient(n))
        return dict(zip(steps, coeffs))

    @np.vectorize
    def shifted_func(self, n, t):
        """
        This function is shifted in order to obtain the
        :param n:
        :param t:
        :return
        """
        return self.func(t) * e**(-n*2*pi*1j*t) * self.DT


#    def __repr__(self) -> str:
#        pass




