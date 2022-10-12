from utils import *


class Bezier:

    def __init__(self, starting_point, control_points: list, end_point):
        self.sp = starting_point
        self.cps = control_points
        self.ep = end_point

    def de_Casteljau(self, points: list, t: int):
        if len(points) == 1:
            in_complex_form = complex(points[0][0], points[0][1])
            return in_complex_form
        else:
            new_points = []
            for i in range(len(points)-1):
                new_points.append(lerp(points[i], points[i+1], t))
            return self.de_Casteljau(new_points, t)


class PolyBezier:

    def __init__(self, beziers: list):
        self.beziers = beziers
        self.num = len(self.beziers)

    def func(self, t):
        index = int(t // (1 / self.num))
        if index == self.num:
            index -= 1
        bez = self.beziers[index]
        points = [bez.sp] + bez.cps + [bez.ep]
        return bez.de_Casteljau(points, t * self.num - index)
