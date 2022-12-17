from math import sqrt


def get_filename(file_name: str):
    return file_name.split(".")[0]


def get_file_content(file_path: str):
    """
    This function grabs the content of the file that is on the input path.
    @param file_path: The absolute or relative path to a file
    @return: The content of the file
    """
    with open(file_path, "r") as f:
        file = f.read()
    return file


def get_extension(file_name: str) -> str:
    """
    This function extracts the extension from a file name.
    @param file_name: A string containing the name of the file
    @return : The extension of the file
    """
    return file_name.split(".")[-1]


def convert_coordinates_to_int(coordinates_in_string: str) -> complex:
    """

    @param coordinates_in_string: This should be in the form (
    @return:
    """
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


def lerp(p0: complex, p1: complex, t: float) -> complex:
    """

    :param p0:
    :param p1:
    :param t:
    :return:
    """
    return (1 - t) * p0 + t * p1


def quadratic(a: float | int, b: float | int, c: float | int):
    try:
        sol1 = ((-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a))
    except (ValueError, ZeroDivisionError) as e:
        sol1 = None
    try:
        sol2 = ((-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a))
    except (ValueError, ZeroDivisionError) as e:
        sol2 = None
    return sol1, sol2


def two_d_dist(p1: complex, p2: complex) -> float:
    return sqrt((p1.real - p2.real) ** 2 + (p1.imag - p2.imag) ** 2)


def arange(start: int, end: int, step: float | int = 1):
    if start > end:
        raise IndexError
    li = []
    num = int((end - start) / step)
    element = start
    for x in range(num):
        li.append(element)
        element += step
    return li
