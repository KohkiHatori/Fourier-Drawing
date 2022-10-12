import re
from utils import *
from config import *
from bezier import Bezier


class SVG:

    def __init__(self, file_content):
        self.content = file_content
        self.path = self.get_path()

    def get_path(self):
        path = re.findall("<path.*/>", self.content, flags=re.DOTALL)[0]
        with_space = re.sub(r"\n", " ", path)
        d = re.findall(r"\".*\"", with_space)[0][1:-1]
        in_coordinates = re.findall(r"[a-zA-z]?-?\d+\.?\d*\s-?\d+\.?\d*z?", d)
        return in_coordinates

    def parse_path(self):
        current_point = np.array([0, 0])
        initial_point = np.array([0, 0])
        relative_coordinates = False
        l_not_c = False
        funcs = []
        points_list = []
        for index, point in enumerate(self.path):
            has_letter = re.search("[a-zA-z]", point)
            if has_letter:
                letter = point[has_letter.start():has_letter.end()]
                point_in_int = convert_coordinates_to_int(pop_char(point, has_letter.start()))
                if letter.upper() != "Z":
                    relative_coordinates = letter.islower()
                match letter:
                    case "M" | "m":
                        current_point = relative_coordinates * current_point + point_in_int
                        if index == 0:
                            initial_point = current_point
                    case "C" | "c":
                        l_not_c = False
                        points_list = [current_point, relative_coordinates * current_point + point_in_int]
                    case "L" | "l":
                        l_not_c = True
                        new_point = relative_coordinates * current_point + point_in_int
                        funcs.append(Bezier(current_point, [], new_point))
                        current_point = new_point
                    case "z":
                        if l_not_c:
                            new_point = relative_coordinates * current_point + point_in_int
                            funcs.append(Bezier(current_point, [], new_point))
                            current_point = new_point
                        else:
                            new_point = relative_coordinates * current_point + point_in_int
                            points_list.append(new_point)
                            if len(points_list) == 4:
                                current_point = new_point
                                funcs.append(Bezier(points_list[0], points_list[1:-1], points_list[-1]))
                                points_list = []
                        funcs.append(Bezier(current_point, [], initial_point))
            else:
                point_in_int = convert_coordinates_to_int(point)
                if l_not_c:
                    new_point = relative_coordinates * current_point + point_in_int
                    funcs.append(Bezier(current_point, [], new_point))
                    current_point = new_point
                else:
                    new_point = relative_coordinates * current_point + point_in_int
                    points_list.append(new_point)
                    if len(points_list) == 4:
                        current_point = new_point
                        funcs.append(Bezier(points_list[0], points_list[1:-1], points_list[-1]))
                        points_list = [current_point]
        return funcs


if __name__ == "__main__":
    with open("/Users/kohkihatori/NEA/API/pictures/apple.svg", "r") as f:
        file = f.read()
    tes = SVG(file)
    funcs = tes.parse_path()
