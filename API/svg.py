import re
from utils import *
from bezier import Bezier


class SVG:

    def __init__(self, file_content):
        self.content = file_content
        self.funcs = []
        self.path = self.get_path()

    def get_path(self) -> list:
        path = re.findall("<path.*/>", self.content, flags=re.DOTALL)[0]
        with_space = re.sub(r"\n", " ", path)
        d = re.findall(r"\".*\"", with_space)[0][1:-1]
        in_coordinates = re.findall(r"[a-zA-z]?-?\d+\.?\d*\s-?\d+\.?\d*z?", d)
        return in_coordinates

    def parse_path(self) -> list:
        self.current_point = complex(0, 0)
        self.initial_point = complex(0, 0)
        self.relative_coordinates = False
        self.l_not_c = False
        self.points_list = []
        for point in self.path:
            has_letter = re.search("[a-zA-z]", point)
            if has_letter:
                letter = point[has_letter.start():has_letter.end()]
                self.point_in_int = convert_coordinates_to_int(pop_char(point, has_letter.start()))
                if letter.upper() != "Z":
                    self.relative_coordinates = letter.islower()
                match letter:
                    case "M" | "m":
                        self._process_m()
                    case "C" | "c":
                        self._process_c()
                    case "L" | "l":
                        self._process_l()
                    case "z" | "Z":
                        self._process_z()
                    case _:
                        raise SyntaxError("incorrect SVG syntax")
            else:
                self.point_in_int = convert_coordinates_to_int(point)
                self._process_coordinates()
        return self.funcs

    def _process_coordinates(self) -> None:
        if self.l_not_c:
            self._process_coordinates_linear()
        else:
            self._process_coordinates_cubic()

    def _process_coordinates_linear(self) -> None:
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        self.funcs.append(Bezier([self.current_point, new_point]))
        self.current_point = new_point

    def _process_coordinates_cubic(self) -> None:
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        self.points_list.append(new_point)
        if len(self.points_list) == 4:
            self.current_point = new_point
            self.funcs.append(Bezier(self.points_list))
            self.points_list = [self.current_point]

    def _process_m(self) -> None:
        self.current_point = self.relative_coordinates * self.current_point + self.point_in_int
        # If there are already Bezier curves in self.funcs, rearrange it so that the pen tip doesn't have to "jump" a
        # long distance
        if len(self.funcs) > 0:
            shortest = self._get_shortest()
            self.rearrange(shortest)
        self.initial_point = self.current_point

    def _process_c(self) -> None:
        self.l_not_c = False
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        self.points_list = [self.current_point, new_point]

    def _process_l(self) -> None:
        self.l_not_c = True
        new_point = self.relative_coordinates * self.current_point + self.point_in_int
        self.funcs.append(Bezier([self.current_point, new_point]))
        self.current_point = new_point

    def _process_z(self) -> None:
        self._process_coordinates()
        self.funcs.append(Bezier([self.current_point, self.initial_point]))
        self.current_point = self.initial_point

    def _get_shortest(self):
        dists = []
        for bez in self.funcs:
            point = bez.points[-1]
            dists.append(two_d_dist(self.current_point, point))
        return dists.index(min(dists))

    def rearrange(self, shortest):
        self.funcs = self.funcs[shortest+1:] + self.funcs[:shortest+1]


#    def __repr__(self) -> str:
#        return f""


if __name__ == "__main__":
    with open("/Users/kohkihatori/NEA/API/pictures/apple.svg", "r") as f:
        file = f.read()
    tes = SVG(file)
    funcs = tes.parse_path()
