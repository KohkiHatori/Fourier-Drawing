from math import e, pi


class ComplexVector:

    def __init__(self, coefficient: complex, n: int):
        self.coefficient = coefficient
        self.n = n

    def func(self, t) -> float:
        return self.coefficient * (e ** (self.n * 2 * pi * 1j * t))

    def __repr__(self):
        return f"n: {self.n} coeff: {self.coefficient}"
