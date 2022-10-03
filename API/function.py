from config import *


class Function:

    def __init__(self, value_dict):
        self.value_dict = value_dict

    def get_coefficient(self, n):
        steps = np.arange(0, 1+DT, DT)
        out = sum(self.shifted_func(self, n, steps))
        return out

    def get_coefficients(self):
        start = -round(NUM/2 - 1)
        coeffs = []
        steps = np.arange(start, start+NUM)
        for n in steps:
            coeffs.append(self.get_coefficient(n))
        return dict(zip(steps, coeffs))

    def func(self, t):
        return self.value_dict[t]

    @np.vectorize
    def shifted_func(self, n, t):
        return self.func(t) * E**(-n*2*PI*1j*t) * DT


def function_sampler(function):
    pass


if __name__ == "__main__":
    myfunc = lambda x: complex(math.cos(2*PI*x), (math.sin(2*PI*x)))
    values = [myfunc(x) for x in np.arange(0, 1+DT, DT)]
    vdict = dict(zip(np.arange(0, 1+DT, DT), values))
    func = Function(vdict)
    coeffs = func.get_coefficients()


