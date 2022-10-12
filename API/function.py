from config import *


class Function:
    """

    """

    def __init__(self, value_dict):
        self.value_dict = value_dict
        self.xlim, self.ylim = self.get_lims()

    def get_coefficient(self, n):
        """
        This function calculates the coefficient for a rotating vector with a frequency of n
        :param n: The frequency of the rotaing vector
        :return: The coefficient
        """
        steps = np.arange(0, 1+DT, DT)
        coefficient = sum(self.shifted_func(self, n, steps))
        return coefficient

    def get_coefficients(self):
        """
        This function gets a coefficient for each vector.
        :return: A dictionary with keys "steps" and values "coeffs"
        """
        start = -round(NUM/2 - 1)
        # The middle value of frequency should be 0, so the minimum frequency is "start"
        # e.g. If the NUM is 10, the minimum frequency is -4.
        coeffs = []
        steps = np.arange(start, start+NUM)
        for n in steps:
            coeffs.append(self.get_coefficient(n))
        return dict(zip(steps, coeffs))

    def func(self, t):
        """
        This function acts exactly the same as the original function.
        The purpose of this function is to refer to the self.value_dict dictionary
        :param t: The variable t.
        :return: The value of the function at the input t.
        """
        return self.value_dict[t]

    @np.vectorize
    def shifted_func(self, n, t):
        """
        This function is shifted in order to obtain the
        :param n:
        :param t:
        :return:
        """
        return self.func(t) * E**(-n*2*PI*1j*t) * DT

    def get_lims(self):
        """
        :return: The maximum and minimum values of real and imaginary values.
        """
        vals = self.value_dict.values()
        real = [val.real for val in vals]
        imag = [val.imag for val in vals]
        xlim = (min(real), max(real))
        ylim = (min(imag), max(imag))
        return xlim, ylim


def function_sampler(function):
    pass


if __name__ == "__main__":
    myfunc = lambda x: complex(math.cos(2*PI*x), (math.sin(2*PI*x)))
    values = [myfunc(x) for x in np.arange(0, 1+DT, DT)]
    vdict = dict(zip(np.arange(0, 1+DT, DT), values))
    func = Function(vdict)
    coeffs = func.get_coefficients()


