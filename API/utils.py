import math

def get_filename(file_name: str):
    return file_name.split(".")[0]


def get_file_content(file_path):
    with open(file_path, "r") as f:
        file = f.read()
    return file


def get_extension(file_name: str):
    return file_name.split(".")[-1]


def convert_coordinates_to_int(coordinates_in_string: str) -> complex:
    points = list(map(float, (coordinates_in_string.split())))
    if len(points) == 2:
        coordinates = complex(points[0], points[1])
    else:
        raise SyntaxError("There should only be two coordinates")
    return coordinates


def pop_char(string: str, pos) -> str:
    li = list(string)
    li.pop(pos)
    return "".join(li)


def lerp(p0: complex, p1: complex, t: float):
    """

    :param p0:
    :param p1:
    :param t:
    :return:
    """
    return (1 - t) * p0 + t * p1


def two_d_dist(p1: complex, p2: complex) -> float:
    return math.sqrt((p1.real-p2.real)**2 + (p1.real-p2.real)**2)

if __name__ == "__main__":
    print(get_filename("2022-10-18 16/26/40.864833.png"))