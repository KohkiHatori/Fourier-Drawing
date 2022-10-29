from utils import *


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

    def de_Casteljau(self, points: list, t: int):
        if len(points) == 1:
            in_complex_form = complex(points[0][0], points[0][1])
            return in_complex_form
        else:
            new_points = []
            for i in range(len(points) - 1):
                new_points.append(lerp(points[i], points[i + 1], t))
            return self.de_Casteljau(new_points, t)

    def __repr__(self) -> str:
        out = f"{self.degree[len(self.points)]} Bezier Curve: "
        for index, point in enumerate(self.points):
            out += f"Point{index+1}: ({point[0]}, {point[1]}) "
        return out


class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        self.num = len(self.beziers)

    def func(self, t) -> complex:
        index = int(t // (1 / self.num))
        if index == self.num:
            index -= 1
        bez = self.beziers[index]
        return bez.de_Casteljau(bez.points, t * self.num - index)

    def __repr__(self) -> str:
        return f"PolyBezier object consisting of {self.num} bezier curves"

    def __len__(self) -> int:
        return self.num
